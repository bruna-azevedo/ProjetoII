// Script do sistema Dance Academy
// Mostra automaticamente o horário final da reserva antes do envio do formulário.

document.addEventListener('DOMContentLoaded', function () {
    const formularios = document.querySelectorAll('form');

    formularios.forEach(function (formulario) {
        const campoHorario = formulario.querySelector('input[name="horario"]');
        const campoDuracao = formulario.querySelector('select[name="duracao_minutos"]');

        if (!campoHorario || !campoDuracao) {
            return;
        }

        const preview = document.createElement('div');
        preview.className = 'preview-horario';
        preview.textContent = 'Selecione o horário de início e a duração para ver o horário final.';

        campoDuracao.insertAdjacentElement('afterend', preview);

        function formatarHora(totalMinutos) {
            const minutosDia = 24 * 60;
            const minutosAjustados = ((totalMinutos % minutosDia) + minutosDia) % minutosDia;
            const horas = Math.floor(minutosAjustados / 60).toString().padStart(2, '0');
            const minutos = (minutosAjustados % 60).toString().padStart(2, '0');
            return `${horas}:${minutos}`;
        }

        function atualizarPreview() {
            const horario = campoHorario.value;
            const duracao = Number(campoDuracao.value);

            if (!horario || !duracao) {
                preview.textContent = 'Selecione o horário de início e a duração para ver o horário final.';
                return;
            }

            const partes = horario.split(':');
            const hora = Number(partes[0]);
            const minuto = Number(partes[1]);
            const inicioEmMinutos = hora * 60 + minuto;
            const fimEmMinutos = inicioEmMinutos + duracao;
            const horarioFinal = formatarHora(fimEmMinutos);

            preview.textContent = `A reserva ficará das ${horario} às ${horarioFinal}.`;
        }

        campoHorario.addEventListener('input', atualizarPreview);
        campoDuracao.addEventListener('change', atualizarPreview);
        atualizarPreview();
    });
});
