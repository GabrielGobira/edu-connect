
const pageContent = document.getElementById("page-content");
const pageTitle = document.getElementById("page-title");

const menuItems = document.querySelectorAll(".menu-item");

function mostrarPagina(pagina) {
    menuItems.forEach((item) => {
        item.classList.toggle("active", item.dataset.page === pagina);
    });

    if (pagina === "alunos") {
        pageTitle.textContent = "Cadastrar aluno";
        carregarPaginaAlunos();
    } else {
        const nomes = {
            frequencia: "Frequência",
            notas: "Notas",
            ocorrencias: "Ocorrências"
        };

        pageTitle.textContent = nomes[pagina];
        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>${nomes[pagina]}</h2>
                <p>Esta funcionalidade será implementada nas próximas etapas.</p>
            </div>
        `;
    }
}

async function carregarPaginaAlunos() {
    pageContent.innerHTML = `
        <div class="welcome-message">
            <h2>Carregando alunos...</h2>
        </div>
    `;

    try {
        const alunos = await apiRequest("/alunos");

        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Novo aluno</h2>
                <p>Preencha os dados para cadastrar um aluno.</p>

                <form id="form-aluno">
                    <label for="nome">Nome completo</label>
                    <input type="text" id="nome" name="nome" required>

                    <label for="matricula">Matrícula</label>
                    <input type="text" id="matricula" name="matricula" required>

                    <label for="turma">Turma</label>
                    <input type="text" id="turma" name="turma" required>

                    <button type="submit">Cadastrar aluno</button>
                </form>

                <p id="mensagem"></p>
            </div>

            <div class="welcome-message">
                <h2>Alunos cadastrados</h2>
                <div id="lista-alunos"></div>
            </div>
        `;

        exibirAlunos(alunos);
        configurarFormulario();

    } catch (error) {
        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Não foi possível carregar os alunos.</h2>
                <p>Verifique se o servidor da API está em execução.</p>
            </div>
        `;
    }
}

function exibirAlunos(alunos) {
    const lista = document.getElementById("lista-alunos");

    if (!Array.isArray(alunos) || alunos.length === 0) {
        lista.textContent = "Nenhum aluno cadastrado.";
        return;
    }

    const tabela = document.createElement("table");
    tabela.innerHTML = `
        <thead>
            <tr>
                <th>Nome</th>
                <th>Matrícula</th>
                <th>Turma</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const corpo = tabela.querySelector("tbody");

    alunos.forEach((aluno) => {
        const linha = document.createElement("tr");

        [aluno.nome, aluno.matricula, aluno.turma].forEach((valor) => {
            const celula = document.createElement("td");
            celula.textContent = valor ?? "";
            linha.appendChild(celula);
        });

        corpo.appendChild(linha);
    });

    lista.replaceChildren(tabela);
}

function configurarFormulario() {
    const formulario = document.getElementById("form-aluno");

    formulario.addEventListener("submit", async (event) => {
        event.preventDefault();

        const dados = {
            nome: formulario.nome.value.trim(),
            matricula: formulario.matricula.value.trim(),
            turma: formulario.turma.value.trim()
        };

        const mensagem = document.getElementById("mensagem");

        try {
            await apiRequest("/alunos", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mensagem.textContent = "Aluno cadastrado com sucesso!";
            formulario.reset();

            const alunosAtualizados = await apiRequest("/alunos");
            exibirAlunos(alunosAtualizados);

        } catch (error) {
            mensagem.textContent = "Não foi possível cadastrar. Verifique os dados e a API.";
        }
    });
}

menuItems.forEach((item) => {
    item.addEventListener("click", () => {
        mostrarPagina(item.dataset.page);
    });
});

mostrarPagina("alunos");
