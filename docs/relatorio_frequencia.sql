SELECT
    alunos.nome AS aluno,
    alunos.turma,
    COUNT(frequencias.id) AS total_aulas,
    SUM(CASE
        WHEN frequencias.presente = 1 THEN 1
        ELSE 0
    END) AS presencas,
    SUM(CASE
        WHEN frequencias.presente = 0 THEN 1
        ELSE 0
    END) AS faltas,
    CASE
        WHEN COUNT(frequencias.id) = 0 THEN NULL
        ELSE ROUND(
            100.0 * SUM(CASE
                WHEN frequencias.presente = 1 THEN 1
                ELSE 0
            END) / COUNT(frequencias.id),
            2
        )
    END AS percentual_presenca
FROM alunos
LEFT JOIN frequencias
    ON alunos.id = frequencias.aluno_id
GROUP BY alunos.id, alunos.nome, alunos.turma
ORDER BY alunos.nome;