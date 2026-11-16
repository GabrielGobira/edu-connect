
const API_URL = "http://127.0.0.1:8000";

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                ...options.headers
            }
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error || `Erro HTTP: ${response.status}`);
        }

        if (response.status === 204) {
            return null;
        }

        return await response.json();

    } catch (error) {
        console.error("Erro na comunicação com a API:", error);
        throw error;
    }
}
