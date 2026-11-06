// Cool Days — petits plus en JavaScript, sans dépendance.
// Le site fonctionne sans : menu visible, photos ouvertes dans un nouvel onglet,
// formulaire envoyé via le logiciel de messagerie.

(function () {
  "use strict";

  var LANG = (document.documentElement.lang || "fr").slice(0, 2);
  var TXT = {
    fr: { photo: "Photo agrandie", close: "Fermer", prev: "Photo précédente", next: "Photo suivante",
          subject: "Demande Cool Days", sent: "Votre messagerie s'ouvre avec le message prêt. Il ne reste qu'à l'envoyer.",
          f: ["Nom", "E-mail", "Téléphone", "Formule", "Arrivée", "Départ", "Nombre de personnes"] },
    nl: { photo: "Vergrote foto", close: "Sluiten", prev: "Vorige foto", next: "Volgende foto",
          subject: "Aanvraag Cool Days", sent: "Uw e-mailprogramma opent met het bericht klaar. U hoeft het alleen nog te versturen.",
          f: ["Naam", "E-mail", "Telefoon", "Keuze", "Aankomst", "Vertrek", "Aantal personen"] },
    de: { photo: "Vergrößertes Foto", close: "Schließen", prev: "Vorheriges Foto", next: "Nächstes Foto",
          subject: "Anfrage Cool Days", sent: "Ihr E-Mail-Programm öffnet sich mit der fertigen Nachricht. Sie müssen sie nur noch senden.",
          f: ["Name", "E-Mail", "Telefon", "Wunsch", "Anreise", "Abreise", "Anzahl Personen"] }
  }[LANG] || null;
  if (!TXT) TXT = { photo: "Photo", close: "×", prev: "‹", next: "›", subject: "Cool Days", sent: "", f: ["", "", "", "", "", "", ""] };

  // ---------- Menu mobile ----------
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.classList.contains("is-open")) {
        header.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  // ---------- Visionneuse de photos ----------
  var links = Array.prototype.slice.call(document.querySelectorAll(".gallery a"));
  if (links.length && typeof HTMLDialogElement === "function") {
    var dialog = document.createElement("dialog");
    dialog.className = "lightbox";
    dialog.setAttribute("aria-label", TXT.photo);
    dialog.innerHTML =
      '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button type="button" class="lb-btn lb-close" aria-label="' + TXT.close + '">' + icon("M18 6 6 18M6 6l12 12") + "</button>" +
      '<button type="button" class="lb-btn lb-prev" aria-label="' + TXT.prev + '">' + icon("M15 18l-6-6 6-6") + "</button>" +
      '<button type="button" class="lb-btn lb-next" aria-label="' + TXT.next + '">' + icon("M9 18l6-6-6-6") + "</button>";
    document.body.appendChild(dialog);

    var img = dialog.querySelector("img");
    var caption = dialog.querySelector("figcaption");
    var current = 0;
    // On ne navigue qu'entre les photos de la même galerie.
    var group = links;

    var show = function (i) {
      current = (i + group.length) % group.length;
      var a = group[current];
      var thumb = a.querySelector("img");
      img.src = a.getAttribute("href");
      img.alt = thumb ? thumb.alt : "";
      caption.textContent = (thumb && thumb.alt ? thumb.alt + " · " : "") + (current + 1) + " / " + group.length;
    };

    links.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        var gallery = a.closest(".gallery");
        group = Array.prototype.slice.call(gallery.querySelectorAll("a"));
        show(group.indexOf(a));
        dialog.showModal();
      });
    });

    dialog.querySelector(".lb-close").addEventListener("click", function () { dialog.close(); });
    dialog.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
    dialog.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });

    // Glisser du doigt sur mobile
    var startX = null;
    dialog.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
    dialog.addEventListener("touchend", function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
      startX = null;
    });
  }

  function icon(d) {
    return '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + d + '"/></svg>';
  }

  // ---------- Formulaire de contact ----------
  // Pas de serveur : on prépare un e-mail dans le logiciel de messagerie du visiteur.
  var form = document.querySelector("#contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) return;
      e.preventDefault();
      var get = function (name) {
        var el = form.elements[name];
        return el && el.value ? el.value.trim() : "";
      };
      var names = ["nom", "email", "telephone", "formule", "arrivee", "depart", "personnes"];
      var lines = names.map(function (n, i) { return TXT.f[i] + " : " + get(n); });
      lines.push("", get("message"));
      var subject = TXT.subject + (get("arrivee") ? " — " + get("arrivee") : "") + " — " + get("nom");
      var href = "mailto:" + form.dataset.to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      var status = form.querySelector(".form-status");
      if (status) {
        status.textContent = TXT.sent;
      }
    });
  }
})();
