select u.nome as usuario,
       count(t.id_tarefa) as total_tarefas,
       sum(case when t.status = 'Concluida' then 1 else 0 end) as concluidas,
       nvl(sum(t.horas_gastas), 0) as total_horas,
       nvl(round(avg(t.horas_gastas), 2), 0) as media_horas
from usuario u
left join tarefa t on t.id_usuario = u.id_usuario
group by u.id_usuario, u.nome
order by total_horas desc, u.nome
