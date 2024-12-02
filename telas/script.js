console.log("js carregado");
document.addEventListener("DOMContentLoaded", () => {
    const menuItems = document.querySelectorAll('.left-menu li a');

    menuItems.forEach(menuItem => {
        menuItem.addEventListener('click', (event) => {
            event.preventDefault();

            const janelaExistente = document.querySelector('.janela-opcoes');
            if (janelaExistente) janelaExistente.remove();

            const janela = document.createElement('div');
            janela.className = 'janela-opcoes';
            janela.textContent = "Janela de Teste";

            document.body.appendChild(janela);

            const { clientX, clientY } = event;
            janela.style.position = 'absolute';
            janela.style.top = `${clientY}px`;
            janela.style.left = `${clientX}px`;

            janela.style.backgroundColor = '#fff';
            janela.style.border = '1px solid #000';
            janela.style.padding = '10px';
            janela.style.boxShadow = '0px 4px 6px rgba(0, 0, 0, 0.1)';
        });
    });
});

//comentario