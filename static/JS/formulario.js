// Clase principal que gestiona el formulario de bienestar emocional
class FormularioBienestar {
    /**
     * Constructor que recibe las preguntas y configura los elementos del DOM.
     * @param {string[]} preguntas - Lista de enunciados del cuestionario.
     */
    constructor(preguntas) {
        this.preguntas = preguntas;
        this.contenedor = document.getElementById('preguntas');  // Contenedor de las preguntas
        this.formulario = document.getElementById('formulario'); // Elemento del formulario
    }

    /**
     * Método que se ejecuta al iniciar: muestra bienvenida, genera preguntas y configura evento submit.
     */
    iniciar() {
        this.mostrarMensajeBienvenida();
        this.generarPreguntas();
        this.formulario.addEventListener('submit', (e) => this.enviarFormulario(e));
    }

    /**
     * Muestra una alerta inicial informativa usando SweetAlert2.
     */
    mostrarMensajeBienvenida() {
        Swal.fire({
            title: 'Bienvenido',
            html: `
                <p>Este cuestionario es totalmente <strong>anónimo</strong>.</p>
                <p>Hace parte de un proyecto para la materia de Computación en la nube, que hace parte de la <strong>Corporación Universitaria Iberoamericana</strong>.</p>
                <p style="color: red; font-weight: bold;">Al enviar las respuestas, la página se cerrará 5 segundos después del envío</p>
            `,
            icon: 'info',
            confirmButtonText: 'Entendido'
        });
    }

    /**
     * Genera dinámicamente las preguntas con sus opciones de respuesta tipo radio.
     */
    generarPreguntas() {
        this.preguntas.forEach((texto, index) => {
            const numero = index + 1;
            const div = document.createElement('div');
            const etiquetas = ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"];

            // Construcción de las opciones tipo radio
            const opciones = etiquetas.map((etiqueta, i) => {
                const valor = i + 1;
                return `
                    <label class="radio-wrap">
                        <input type="radio" name="respuesta${numero}" value="${valor}" required>
                        <span>${valor} - ${etiqueta}</span>
                    </label>
                `;
            }).join('');

            // Inserta la pregunta y sus opciones en el contenedor
            div.innerHTML = `
                <label>${numero}. ${texto}</label><br>
                <div class="opciones-radio">${opciones}</div><br><br>
            `;
            this.contenedor.appendChild(div);
        });
    }

    /**
     * Obtiene las respuestas seleccionadas por el usuario.
     * @returns {Object} Diccionario con clave "preguntaN" y valor de 1 a 5.
     */
    obtenerRespuestas() {
        const respuestas = {};
        this.preguntas.forEach((_, index) => {
            const qIndex = index + 1;
            const seleccion = document.querySelector(`input[name="respuesta${qIndex}"]:checked`);
            respuestas[`pregunta${qIndex}`] = seleccion ? parseInt(seleccion.value) : null;
        });
        return respuestas;
    }

    /**
     * Envía las respuestas al backend y maneja la respuesta del servidor.
     * @param {Event} e - Evento del formulario.
     */
    async enviarFormulario(e) {
        e.preventDefault();

        const respuestas = this.obtenerRespuestas();
        const incompletas = Object.values(respuestas).some(v => v === null || isNaN(v));

        // Verifica si todas las preguntas han sido respondidas
        if (incompletas) {
            Swal.fire({
                icon: 'warning',
                title: 'Faltan respuestas',
                text: 'Por favor, responda todas las preguntas antes de enviar.',
                confirmButtonText: 'OK'
            });
            return;
        }

        try {
            // Envía los datos al backend con fetch
            const response = await fetch('/api/respuestas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(respuestas)
            });

            const resultado = await response.json();

            // Si la respuesta fue exitosa
            if (response.ok) {
                await Swal.fire({
                    icon: 'success',
                    title: '¡Respuestas enviadas!',
                    text: resultado.mensaje || 'Tus respuestas se han enviado correctamente.',
                    confirmButtonText: 'Aceptar'
                });

                // Cierra la pestaña luego de 5 segundos
                setTimeout(() => window.close(), 5000);

            } else {
                // Error recibido desde el backend
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: resultado.mensaje || 'Ocurrió un error al enviar las respuestas.',
                    confirmButtonText: 'OK'
                });
            }

        } catch (error) {
            // Error de conexión o inesperado
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo enviar la información. Intenta más tarde.',
                confirmButtonText: 'OK'
            });
        }
    }
}

// Lista de preguntas del cuestionario
const preguntas = [
    "Me he sentido motivado para realizar mis tareas laborales.",
    "He sentido que manejo bien el estrés durante mi jornada.",
    "Me siento emocionalmente agotado al final del día.",
    "Me he sentido valorado por mi equipo de trabajo.",
    "Mi entorno de trabajo me permite concentrarme sin interrupciones constantes.",
    "Cuento con los recursos necesarios para cumplir con mis responsabilidades.",
    "La carga de trabajo ha sido adecuada esta semana.",
    "He tenido espacios suficientes para tomar pausas o descansos.",
    "Siento que puedo contar con mis compañeros si tengo un mal día.",
    "Me siento escuchado cuando comparto inquietudes en el equipo.",
    "Mis superiores muestran interés por el bienestar del equipo.",
    "He logrado mantener un equilibrio saludable entre mi vida laboral y personal.",
    "El trabajo no ha interferido negativamente con mi tiempo personal.",
    "En general, me he sentido bien emocionalmente esta semana.",
    "Me he sentido satisfecho con mis logros laborales recientes.",
    "Considero que esta semana ha sido positiva para mi desarrollo personal y profesional."
];

// Ejecuta la aplicación cuando el DOM esté completamente cargado
window.addEventListener('DOMContentLoaded', () => {
    const app = new FormularioBienestar(preguntas);
    app.iniciar();
});
