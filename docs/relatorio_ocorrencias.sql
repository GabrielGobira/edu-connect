SELECT
    alunos.nome AS aluno,
    alunos.matricula,
    alunos.turma,
    ocorrencias.data,
    COALESCE(
        ocorrencias.descricao,
        'Nenhuma ocorrência registrada'
    ) AS ocorrencia
FROM alunos
LEFT JOIN ocorrencias
    ON alunos.id = ocorrencias.aluno_id
ORDER BY alunos.nome, ocorrencias.data;