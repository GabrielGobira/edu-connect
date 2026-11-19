const pageContent = document.getElementById("page-content");
const pageTitle = document.getElementById("page-title");

const menuItems = document.querySelectorAll(".menu-item");

const loginScreen = document.getElementById("login-screen");
const appContainer = document.getElementById("app-container");
const formLogin = document.getElementById("form-login");
const mensagemLogin = document.getElementById("mensagem-login");
const btnLogout = document.getElementById("btn-logout");

// Controla a exibição das telas
function mostrarSistema() {
    loginScreen.hidden = true;
    appContainer.hidden = false;
    mostrarPagina("alunos");
}

function mostrarLogin() {
    appContainer.hidden = true;
    loginScreen.hidden = false;
    formLogin.reset();
    mensagemLogin.textContent = "";
}

// Realiza o login
formLogin.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = formLogin.elements.email.value.trim();
    const senha = formLogin.elements.senha.value;

    mensagemLogin.textContent = "Autenticando...";

    try {
        await login(email, senha);

        mensagemLogin.textContent = "";
        mostrarSistema();

    } catch (error) {
        mensagemLogin.textContent =
            error.message || "Não foi possível realizar o login.";
    }
});

// Encerra a sessão
btnLogout.addEventListener("click", () => {
    logout();
    mostrarLogin();
});

// Navegação entre páginas
function mostrarPagina(pagina) {
    menuItems.forEach((item) => {
        item.classList.toggle(
            "active",
            item.dataset.page === pagina
        );
    });

if (pagina === "alunos") {
    pageTitle.textContent = "Cadastrar aluno";
    carregarPaginaAlunos();

} else if (pagina === "frequencia") {
    pageTitle.textContent = "Frequência";
    carregarPaginaFrequencia();

} else if (pagina === "notas") {
    pageTitle.textContent = "Notas";
    carregarPaginaNotas();

} else if (pagina === "ocorrencias") {
    pageTitle.textContent = "Ocorrências";
    carregarPaginaOcorrencias();

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

// Carrega a página de alunos
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
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Exibe a tabela de alunos
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
                <th>Ações</th>
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

        const celulaAcoes = document.createElement("td");

        const botaoEditar = document.createElement("button");
        botaoEditar.textContent = "Editar";
        botaoEditar.className = "btn-editar";
        botaoEditar.type = "button";
        botaoEditar.addEventListener("click", () => editarAluno(aluno));

        const botaoExcluir = document.createElement("button");
        botaoExcluir.textContent = "Excluir";
        botaoExcluir.className = "btn-excluir";
        botaoExcluir.type = "button";
        botaoExcluir.addEventListener("click", () => excluirAluno(aluno.id));

        celulaAcoes.append(botaoEditar, botaoExcluir);
        linha.appendChild(celulaAcoes);

        corpo.appendChild(linha);
    });

    lista.replaceChildren(tabela);
}

// Configura o formulário de cadastro
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
            mensagem.textContent =
                error.message || "Não foi possível cadastrar o aluno.";
        }
    });
}
// Edita os dados de um aluno
async function editarAluno(aluno) {
    const nome = prompt("Nome do aluno:", aluno.nome);
    if (nome === null) return;

    const matricula = prompt("Matrícula:", aluno.matricula);
    if (matricula === null) return;

    const turma = prompt("Turma:", aluno.turma);
    if (turma === null) return;

    const dados = {
        nome: nome.trim(),
        matricula: matricula.trim(),
        turma: turma.trim()
    };

    if (!dados.nome || !dados.matricula || !dados.turma) {
        alert("Preencha todos os campos.");
        return;
    }

    try {
        await apiRequest(`/alunos/${aluno.id}`, {
            method: "PUT",
            body: JSON.stringify(dados)
        });

        alert("Aluno atualizado com sucesso!");
        carregarPaginaAlunos();

    } catch (error) {
        alert(error.message || "Não foi possível atualizar o aluno.");
    }
}

// Exclui um aluno
async function excluirAluno(id) {
    const confirmar = confirm(
        "Tem certeza de que deseja excluir este aluno?"
    );

    if (!confirmar) return;

    try {
        await apiRequest(`/alunos/${id}`, {
            method: "DELETE"
        });

        alert("Aluno excluído com sucesso!");
        carregarPaginaAlunos();

    } catch (error) {
        alert(error.message || "Não foi possível excluir o aluno.");
    }
}

async function carregarPaginaFrequencia() {
    pageContent.innerHTML = `
        <div class="welcome-message">
            <h2>Carregando informações...</h2>
        </div>
    `;

    try {
        const [alunos, frequencias] = await Promise.all([
            apiRequest("/alunos"),
            apiRequest("/frequencias")
        ]);

        const hoje = new Date();
        const dataHoje = [
            hoje.getFullYear(),
            String(hoje.getMonth() + 1).padStart(2, "0"),
            String(hoje.getDate()).padStart(2, "0")
        ].join("-");

        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Registrar frequência</h2>
                <p>Selecione o aluno e informe a situação da presença.</p>

                <form id="form-frequencia">

                    <label for="aluno-frequencia">Aluno</label>
                    <select id="aluno-frequencia" required>
                        <option value="">Selecione um aluno</option>
                        ${alunos.map(aluno => `
                            <option value="${aluno.id}">
                                ${aluno.nome} - ${aluno.turma}
                            </option>
                        `).join("")}
                    </select>

                    <label for="data-frequencia">Data</label>
                    <input
                        type="date"
                        id="data-frequencia"
                        value="${dataHoje}"
                        required
                    >

                    <label for="presente">Situação</label>
                    <select id="presente" required>
                        <option value="true">Presente</option>
                        <option value="false">Ausente</option>
                    </select>

                    <button type="submit">Registrar frequência</button>

                    <p id="mensagem-frequencia"></p>
                </form>
            </div>

            <div class="welcome-message">
                <h2>Histórico de frequência</h2>
                <div id="lista-frequencias"></div>
            </div>
        `;

        exibirFrequencias(frequencias, alunos);
        configurarFormularioFrequencia();

    } catch (error) {
        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Não foi possível carregar a frequência.</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function exibirFrequencias(frequencias, alunos) {
    const lista = document.getElementById("lista-frequencias");

    if (!frequencias.length) {
        lista.textContent = "Nenhum registro de frequência encontrado.";
        return;
    }

    const tabela = document.createElement("table");

    tabela.innerHTML = `
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Data</th>
                <th>Situação</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const corpo = tabela.querySelector("tbody");

    frequencias.forEach(registro => {
        const aluno = alunos.find(
            item => item.id === registro.aluno_id
        );

        const linha = document.createElement("tr");

       const valores = [
    aluno ? aluno.nome : `Aluno ${registro.aluno_id}`,
    registro.data
];

valores.forEach(valor => {
    const celula = document.createElement("td");
    celula.textContent = valor;
    linha.appendChild(celula);
});

// Destaca a situação da frequência
const celulaSituacao = document.createElement("td");
const situacao = document.createElement("span");

situacao.textContent = registro.presente ? "Presente" : "Ausente";
situacao.className = registro.presente
    ? "status-presente"
    : "status-ausente";

celulaSituacao.appendChild(situacao);
linha.appendChild(celulaSituacao);

        corpo.appendChild(linha);
    });

    lista.replaceChildren(tabela);
}

function configurarFormularioFrequencia() {
    const formulario = document.getElementById("form-frequencia");

    formulario.addEventListener("submit", async event => {
        event.preventDefault();

        const dados = {
            aluno_id: Number(
                document.getElementById("aluno-frequencia").value
            ),
            data: document.getElementById("data-frequencia").value,
            presente:
                document.getElementById("presente").value === "true"
        };

        const mensagem = document.getElementById(
            "mensagem-frequencia"
        );

        try {
            await apiRequest("/frequencias", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mensagem.textContent = "Frequência registrada com sucesso!";

            const alunos = await apiRequest("/alunos");
            const frequencias = await apiRequest("/frequencias");

            exibirFrequencias(frequencias, alunos);

        } catch (error) {
            mensagem.textContent =
                error.message || "Não foi possível registrar a frequência.";
        }
    });
}

async function carregarPaginaNotas() {
    pageContent.innerHTML = `
        <div class="welcome-message">
            <h2>Carregando informações...</h2>
        </div>
    `;

    try {
        const [alunos, notas] = await Promise.all([
            apiRequest("/alunos"),
            apiRequest("/notas")
        ]);

        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Lançar nota</h2>
                <p>Selecione o aluno e informe a disciplina e a nota.</p>

                <form id="form-nota">
                    <label for="aluno-nota">Aluno</label>
                    <select id="aluno-nota" required>
                        <option value="">Selecione um aluno</option>
                        ${alunos.map(aluno => `
                            <option value="${aluno.id}">
                                ${aluno.nome} - ${aluno.turma}
                            </option>
                        `).join("")}
                    </select>

                    <label for="disciplina-nota">Disciplina</label>
                    <input
                        type="text"
                        id="disciplina-nota"
                        maxlength="100"
                        required
                    >

                    <label for="valor-nota">Nota (0 a 10)</label>
                    <input
                        type="number"
                        id="valor-nota"
                        min="0"
                        max="10"
                        step="0.1"
                        required
                    >

                    <button type="submit">Salvar nota</button>
                    <p id="mensagem-nota"></p>
                </form>
            </div>

            <div class="welcome-message">
                <h2>Notas cadastradas</h2>
                <div id="lista-notas"></div>
            </div>
        `;

        exibirNotas(notas, alunos);
        configurarFormularioNota();

    } catch (error) {
        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Não foi possível carregar as notas.</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function exibirNotas(notas, alunos) {
    const lista = document.getElementById("lista-notas");

    if (!Array.isArray(notas) || notas.length === 0) {
        lista.textContent = "Nenhuma nota cadastrada.";
        return;
    }

    const tabela = document.createElement("table");

    tabela.innerHTML = `
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Disciplina</th>
                <th>Nota</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const corpo = tabela.querySelector("tbody");

    notas.forEach(registro => {
        const aluno = alunos.find(
            item => item.id === registro.aluno_id
        );

        const linha = document.createElement("tr");

     const valores = [
    aluno ? aluno.nome : `Aluno ${registro.aluno_id}`,
    registro.disciplina
];

valores.forEach(valor => {
    const celula = document.createElement("td");
    celula.textContent = valor;
    linha.appendChild(celula);
});

// Indicador visual da nota
const celulaNota = document.createElement("td");
const indicador = document.createElement("span");
const nota = Number(registro.nota);

indicador.textContent = nota.toFixed(1);

if (nota >= 7) {
    indicador.className = "nota-alta";
} else if (nota >= 5) {
    indicador.className = "nota-media";
} else {
    indicador.className = "nota-baixa";
}

celulaNota.appendChild(indicador);
linha.appendChild(celulaNota);

        corpo.appendChild(linha);
    });

    lista.replaceChildren(tabela);
}

function configurarFormularioNota() {
    const formulario = document.getElementById("form-nota");

    formulario.addEventListener("submit", async event => {
        event.preventDefault();

        const dados = {
            aluno_id: Number(
                document.getElementById("aluno-nota").value
            ),
            disciplina: document.getElementById("disciplina-nota").value.trim(),
            nota: Number(
                document.getElementById("valor-nota").value
            )
        };

        const mensagem = document.getElementById("mensagem-nota");

        try {
            await apiRequest("/notas", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mensagem.textContent = "Nota salva com sucesso!";

            const [alunos, notas] = await Promise.all([
                apiRequest("/alunos"),
                apiRequest("/notas")
            ]);

            exibirNotas(notas, alunos);

            formulario.reset();

        } catch (error) {
            mensagem.textContent =
                error.message || "Não foi possível salvar a nota.";
        }
    });
}

async function carregarPaginaOcorrencias() {
    pageContent.innerHTML = `
        <div class="welcome-message">
            <h2>Carregando informações...</h2>
        </div>
    `;

    try {
        const [alunos, ocorrencias] = await Promise.all([
            apiRequest("/alunos"),
            apiRequest("/ocorrencias")
        ]);

        const hoje = new Date();
        const dataHoje = [
            hoje.getFullYear(),
            String(hoje.getMonth() + 1).padStart(2, "0"),
            String(hoje.getDate()).padStart(2, "0")
        ].join("-");

        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Registrar ocorrência</h2>
                <p>Informe o aluno e descreva a ocorrência.</p>

                <form id="form-ocorrencia">
                    <label for="aluno-ocorrencia">Aluno</label>
                    <select id="aluno-ocorrencia" required>
                        <option value="">Selecione um aluno</option>
                        ${alunos.map(aluno => `
                            <option value="${aluno.id}">
                                ${aluno.nome} - ${aluno.turma}
                            </option>
                        `).join("")}
                    </select>

                    <label for="data-ocorrencia">Data</label>
                    <input
                        type="date"
                        id="data-ocorrencia"
                        value="${dataHoje}"
                        required
                    >

                    <label for="descricao-ocorrencia">Descrição</label>
                    <textarea
                        id="descricao-ocorrencia"
                        maxlength="500"
                        rows="4"
                        required
                        placeholder="Descreva a ocorrência..."
                    ></textarea>

                    <button type="submit">Registrar ocorrência</button>
                    <p id="mensagem-ocorrencia"></p>
                </form>
            </div>

            <div class="welcome-message">
                <h2>Histórico de ocorrências</h2>
                <div id="lista-ocorrencias"></div>
            </div>
        `;

        exibirOcorrencias(ocorrencias, alunos);
        configurarFormularioOcorrencia();

    } catch (error) {
        pageContent.innerHTML = `
            <div class="welcome-message">
                <h2>Não foi possível carregar as ocorrências.</h2>
                <p>${error.message}</p>
            </div>
        `;
    }
}

function exibirOcorrencias(ocorrencias, alunos) {
    const lista = document.getElementById("lista-ocorrencias");

    if (!Array.isArray(ocorrencias) || ocorrencias.length === 0) {
        lista.textContent = "Nenhuma ocorrência cadastrada.";
        return;
    }

    const tabela = document.createElement("table");

    tabela.innerHTML = `
        <thead>
            <tr>
                <th>Aluno</th>
                <th>Data</th>
                <th>Descrição</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const corpo = tabela.querySelector("tbody");

    ocorrencias.forEach(registro => {
        const aluno = alunos.find(
            item => item.id === registro.aluno_id
        );

        const linha = document.createElement("tr");

        const valores = [
            aluno ? aluno.nome : `Aluno ${registro.aluno_id}`,
            registro.data,
            registro.descricao
        ];

        valores.forEach(valor => {
            const celula = document.createElement("td");
            celula.textContent = valor;
            linha.appendChild(celula);
        });

        corpo.appendChild(linha);
    });

    lista.replaceChildren(tabela);
}

function configurarFormularioOcorrencia() {
    const formulario = document.getElementById("form-ocorrencia");

    formulario.addEventListener("submit", async event => {
        event.preventDefault();

        const dados = {
            aluno_id: Number(
                document.getElementById("aluno-ocorrencia").value
            ),
            data: document.getElementById("data-ocorrencia").value,
            descricao: document.getElementById("descricao-ocorrencia").value.trim()
        };

        const mensagem = document.getElementById("mensagem-ocorrencia");

        if (!dados.descricao) {
            mensagem.textContent = "Informe uma descrição válida.";
            return;
        }

        try {
            await apiRequest("/ocorrencias", {
                method: "POST",
                body: JSON.stringify(dados)
            });

            mensagem.textContent = "Ocorrência registrada com sucesso!";

            const [alunos, ocorrencias] = await Promise.all([
                apiRequest("/alunos"),
                apiRequest("/ocorrencias")
            ]);

            exibirOcorrencias(ocorrencias, alunos);
            formulario.reset();

        } catch (error) {
            mensagem.textContent =
                error.message || "Não foi possível registrar a ocorrência.";
        }
    });
}

// Eventos do menu
menuItems.forEach((item) => {
    item.addEventListener("click", () => {
        mostrarPagina(item.dataset.page);
    });
});

// Inicialização
if (obterToken()) {
    mostrarSistema();
} else {
    mostrarLogin();
}