select t.id_tarefa as id,
       t.titulo,
       u.nome as usuario,
       c.nome as categoria,
       t.prioridade,
       t.status,
       to_char(t.data_criacao, 'DD/MM/YYYY') as criada_em,
       to_char(t.data_conclusao, 'DD/MM/YYYY') as concluida_em,
       t.horas_gastas as horas
from tarefa t
join usuario u on u.id_usuario = t.id_usuario
join categoria c on c.id_categoria = t.id_categoria
order by t.id_tarefa
