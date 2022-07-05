## O que podemos alterar:

### Mines:

Nenhuma das duas classes (threads) (utilizadas pra produzir oil e uranium (começa em 0, vai no máximo até constraint)). oil_earth e uranium_earth alcançáveis pelas globais (lua não possui e deve receber!)

### Space:

#### Bases (Thread):

Tudo pode ser alterado, exceto o construtor.  
Documentar tudo para ficar mais entendível (docstrings ou comentários sobre o que os métodos fazem).  
Completar toda/quase toda lógica: métodos refuel oil e oranium e run

#### Rocket

Posso/devo alterar apenas nuke e voyage;  
Avaliar onde rockets estão sendo instanciadas (e onde chamo launch?)

### Stars

#### Planet (Thread)

Posso alterar tudo menos construtor

### Globals

Posso alterar, criar mutexes etc tudo aqui.

![Relação entre módulos](https://lh5.googleusercontent.com/FysjW9IAwJHyRJwufpuC5qamcjJN4ZPzEhN_VzpgIiKl8uiWRp-oEax8OTO39J8t_v7epTUOrtS95FRmZ5xlgVFRCWLl53_SUYQU2hzYzDh-TirTXwilhQXJUvisoHaIPUHphHrkw8O0sPe-Bg)

### More info

Lion -> 75 unidades de urânio e 120 unidades de combustível para a base lunar.  
(Dragon e Falcon) -> ogivas nucleares, a partir de 35 unidades de urânio da base de lançamento.  
Cada base:

- Foguetes: (2 para a Lua, 5 para Cabo Canaveral, 5 para Moscou e 1 para Alcântara) (CONSOMEM COMBUSTÍVEL DIFERENTE POR BASE, VER NO MOODLE)
- Uma plataforma de lançamento (um foguete lançado por vez, usar launch aqui)
- Lançamentos aleatórios, exceto da lua (ela notifica quando um recurso acaba)
  Importante: menos de três bombas ao mesmo tempo no planeta, no máximo duas?? por polo
