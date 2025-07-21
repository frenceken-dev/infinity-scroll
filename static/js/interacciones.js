// =======================
//     Activar el Menu
// =======================
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM completamente cargado ✅");

    const toggle = document.querySelector('.usuario-toggle');
    const dropdown = document.querySelector('.usuario-dropdown');

    console.log("toggle:", toggle);  // ¿Es null o un botón?
    console.log("dropdown:", dropdown);  // ¿Existe?

    if (!toggle || !dropdown) {
        console.warn("No se encontró el botón o el contenedor del menú.");
        return;
    }

    toggle.addEventListener('click', (e) => {
        console.log("Click en botón usuario");
        dropdown.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });

    document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        dropdown.classList.remove('open');
        }
    });
});


// =======================
// Configuración CSRF
// =======================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// ===================================================
// Código para Generar Scroll infiníto vista principal
// ===================================================
let page = 1;
let loading = false;
let hasNext = true;

// Obtener el contenedor con scroll interno
const zonaScroll = document.getElementById('zona-scroll');
const grid = document.getElementById('contenedor-videos-imagenes');
const loader = document.getElementById('loader');

if (zonaScroll && grid && loader) {
    
    function cargarMasContenido() {
    if (!hasNext || loading) return;

    loading = true;
    loader.style.display = 'block';

    const urlScroll = grid.dataset.urlScroll;

    // Conservar filtros y búsqueda actuales
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('page', page);
    console.log("Cargando página:", page, urlScroll + "?" + queryParams.toString());

    fetch(`${urlScroll}?${queryParams.toString()}`)
        .then(response => response.json())
        .then(data => {
            grid.insertAdjacentHTML('beforeend', data.html);

            document.querySelectorAll('.video-card, .imagen-card').forEach(card => {
                if (!card.classList.contains('fade-in')) {
                    card.classList.add('fade-in');
                }
            });

            hasNext = data.has_next;
            page += 1;
            loading = false;

            if (!hasNext) {
                loader.innerText = "¡Has llegado al final del contenido!";
            } else {
                loader.style.display = 'none';
            }
        });
    }


    // Escuchar el scroll solo en la zona scrollable
    zonaScroll.addEventListener('scroll', () => {
        if ((zonaScroll.scrollTop + zonaScroll.clientHeight) >= zonaScroll.scrollHeight - 200) {
            cargarMasContenido();
        }
    });

    // Cargar más al iniciar si el contenido es pequeño
    window.addEventListener('load', () => {
        setTimeout(() => {
            if ((zonaScroll.scrollTop + zonaScroll.clientHeight) >= zonaScroll.scrollHeight - 200 && hasNext) {
                cargarMasContenido();
            }
        }, 600);
    });
}
