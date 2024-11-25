// Adiciona o evento de clique nos itens do menu
document.querySelectorAll('.left-menu li a').forEach(menuItem => {
    menuItem.addEventListener('click', (event) => {
        event.preventDefault(); // Evita o redirecionamento padrão
        mostrarJanela(menuItem.textContent.trim()); // Passa o texto do item clicado
    });
});

// Função para criar e exibir a janela
function mostrarJanela(esporte) {
    // Remove qualquer janela existente
    const janelaExistente = document.querySelector('.janela-opcoes');
    if (janelaExistente) janelaExistente.remove();

    // Cria o contêiner da janela
    const janela = document.createElement('div');
    janela.className = 'janela-opcoes';

    // Adiciona conteúdo à janela
    janela.innerHTML = `
        <h4>${esporte}</h4>
        <ul>
            <li><a href="#">Notícias</a></li>
            <li><a href="#">Adicionar aos favoritos</a></li>
        </ul>
    `;

    // Adiciona a janela ao corpo
    document.body.appendChild(janela);

    // Posiciona a janela próximo ao item clicado
    janela.style.top = `${event.pageY}px`;
    janela.style.left = `${event.pageX}px`;

    // Fecha a janela ao clicar fora dela
    document.addEventListener('click', fecharJanela, { once: true });
}

// Função para fechar a janela
function fecharJanela(event) {
    const janela = document.querySelector('.janela-opcoes');
    if (janela && !janela.contains(event.target)) {
        janela.remove();
    }
}