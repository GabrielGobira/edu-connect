
const API_URL = "http://127.0.0.1:8000";

// Recupera o token da sessão atual
function obterToken() {
    return sessionStorage.getItem("educonnect_token");
}

// Realiza o login
async function login(email, senha) {
    const dados = new URLSearchParams();

    dados.append("username", email);
    dados.append("password", senha);

    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: dados
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Erro ao realizar login.");
    }

    const resultado = await response.json();

    sessionStorage.setItem(
        "educonnect_token",
        resultado.access_token
    );

    return resultado;
}

// Encerra a sessão
function logout() {
    sessionStorage.removeItem("educonnect_token");
}

// Realiza requisições para a API
async function apiRequest(endpoint, options = {}) {
    try {
        const token = obterToken();

        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 204) {
            return null;
        }

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));

            if (response.status === 401) {
                logout();
            }

            throw new Error(
                error.detail || `Erro HTTP: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {
        console.error("Erro na comunicação com a API:", error);
        throw error;
    }
}
