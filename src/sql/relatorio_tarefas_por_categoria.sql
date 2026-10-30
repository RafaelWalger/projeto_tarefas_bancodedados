select c.nome as categoria,
       count(t.id_tarefa) as total_tarefas,
       sum(case when t.status = 'Concluida' then 1 else 0 end) as concluidas,
       sum(case when t.status <> 'Concluida' then 1 else 0 end) as em_aberto,
       nvl(sum(t.horas_gastas), 0) as total_horas
from categoria c
left join tarefa t on t.id_categoria = c.id_categoria
group by c.id_categoria, c.nome
order by total_tarefas desc, c.nome
