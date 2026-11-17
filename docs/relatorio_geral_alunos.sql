SELECT
    alunos.id,
    alunos.nome AS aluno,
    alunos.matricula,
    alunos.turma,

    (SELECT ROUND(AVG(n.nota), 2)
     FROM notas n
     WHERE n.aluno_id = alunos.id) AS media_geral,

    (SELECT COUNT(*)
     FROM frequencias f
     WHERE f.aluno_id = alunos.id) AS aulas_registradas,

    (SELECT COUNT(*)
     FROM frequencias f
     WHERE f.aluno_id = alunos.id
       AND f.presente = 1) AS presencas,

    (SELECT COUNT(*)
     FROM frequencias f
     WHERE f.aluno_id = alunos.id
       AND f.presente = 0) AS faltas,

    (SELECT COUNT(*)
     FROM ocorrencias o
     WHERE o.aluno_id = alunos.id) AS total_ocorrencias

FROM alunos
ORDER BY alunos.nome;