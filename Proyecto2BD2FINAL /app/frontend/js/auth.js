export function validarSesionYMostrarHeader() {
    const usuarioId = localStorage.getItem("usuario_id");
    const usuarioNombre = localStorage.getItem("usuario_nombre");
  
    if (!usuarioId) {
      alert("Inicia sesión primero.");
      window.location.href = "login.html";
      return;
    }
  
    fetch("header.html")
      .then(res => res.text())
      .then(html => {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = html;
        document.body.prepend(wrapper);
  
        document.getElementById("usuario-nombre").textContent = `${usuarioNombre}`;
  
        document.getElementById("logout").addEventListener("click", () => {
          localStorage.clear();
          window.location.href = "login.html";
        });
      })
      .catch(err => {
        console.error("No se pudo cargar el header:", err);
      });
  }
  