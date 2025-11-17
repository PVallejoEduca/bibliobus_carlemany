/* Manejo sencillo de sesión en el navegador. */
(function () {
  const STORAGE_KEY = "bibliobusUser";

  function parseUser(raw) {
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (error) {
      console.warn("No se pudo leer el usuario almacenado, se limpia la sesión.");
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }
  }

  function getUser() {
    return parseUser(localStorage.getItem(STORAGE_KEY));
  }

  function setUser(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    syncAuthUI();
  }

  function clearUser() {
    localStorage.removeItem(STORAGE_KEY);
    syncAuthUI();
  }

  function syncAuthUI() {
    const user = getUser();

    document.querySelectorAll("[data-auth-required]").forEach((el) => {
      el.classList.toggle("hidden", !user);
    });

    document.querySelectorAll("[data-login-link]").forEach((link) => {
      if (user) {
        link.classList.add("hidden");
      } else {
        link.classList.remove("hidden");
        link.textContent = "Login";
      }
    });

    document.querySelectorAll("[data-profile-link]").forEach((link) => {
      if (user) {
        link.classList.remove("hidden");
        link.setAttribute("title", `Perfil de ${user.nickname}`);
      } else {
        link.classList.add("hidden");
      }
    });

    document.querySelectorAll("[data-logout]").forEach((btn) => {
      btn.classList.toggle("hidden", !user);
    });
  }

  function initAuthUI() {
    document.querySelectorAll("[data-logout]").forEach((btn) => {
      btn.addEventListener("click", async (event) => {
        event.preventDefault();
        try {
          await fetch("/api/auth/logout", { method: "POST", credentials: "same-origin" });
        } catch (error) {
          console.warn("No se pudo cerrar sesión en el servidor", error);
        }
        clearUser();
      });
    });

    syncAuthUI();
  }

  document.addEventListener("DOMContentLoaded", initAuthUI);

  window.BibliobusAuth = {
    getUser,
    setUser,
    clearUser,
    sync: syncAuthUI,
  };
})();
