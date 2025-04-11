document.addEventListener('DOMContentLoaded', () => {
    // Validação do formulário de contato
    const contatoForm = document.querySelector('#contato form');
    if (contatoForm) {
        contatoForm.addEventListener('submit', (e) => {
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            if (!nome || !email) {
                alert('Por favor, preencha todos os campos!');
                e.preventDefault();
            }
        });
    }

    // Validação do formulário de login
    const loginForm = document.querySelector('#login form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (!username || !password) {
                alert('Por favor, preencha todos os campos!');
                e.preventDefault();
            }
        });
    }

    // Adicionar evento de clique para os botões "Editar"
    const editButtons = document.querySelectorAll('.edit-imovel-btn');
    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const id = button.dataset.id;
            const titulo = button.dataset.titulo;
            const descricao = button.dataset.descricao;
            const preco = button.dataset.preco;
            const localizacao = button.dataset.localizacao;
            const tipo = button.dataset.tipo;
            const imagem = button.dataset.imagem;
            editImovel(id, titulo, descricao, preco, localizacao, tipo, imagem);
        });
    });
});

function editImovel(id, titulo, descricao, preco, localizacao, tipo, imagem) {
    document.getElementById('edit-id').value = id;
    document.getElementById('edit-titulo').value = titulo;
    document.getElementById('edit-descricao').value = descricao;
    document.getElementById('edit-preco').value = preco;
    document.getElementById('edit-localizacao').value = localizacao;
    document.getElementById('edit-tipo').value = tipo;
    document.getElementById('edit-imagem').value = imagem;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}