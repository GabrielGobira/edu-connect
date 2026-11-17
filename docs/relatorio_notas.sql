SELECT
    alunos.nome AS aluno,
    alunos.matricula,
    alunos.turma,
    COUNT(notas.id) AS quantidade_notas,
    ROUND(AVG(notas.nota), 2) AS media_geral,
    CASE
        WHEN AVG(notas.nota) IS NULL THEN 'Sem notas'
        WHEN AVG(notas.nota) >= 7 THEN 'Aprovado por média'
        ELSE 'Abaixo da média'
    END AS situacao
FROM alunos
LEFT JOIN notas
    ON alunos.id = notas.aluno_id
GROUP BY
    alunos.id,
    alunos.nome,
    alunos.matricula,
    alunos.turma
ORDER BY alunos.nome;