# Robô Autônomo de Resgate em Ambiente Simulado

## Descrição

Este projeto tem como objetivo o desenvolvimento de um robô móvel autônomo para operações de resgate em ambientes simulados, utilizando o ROS (Robot Operating System).

O sistema é capaz de explorar o ambiente, realizar mapeamento (SLAM), navegar de forma autônoma e detectar vítimas utilizando visão computacional.

---

## Objetivos

* Implementar navegação autônoma
* Realizar mapeamento do ambiente (SLAM)
* Detectar vítimas utilizando câmera RGB
* Integrar todos os módulos no ROS
* Validar o sistema em ambiente simulado

---

## Tecnologias Utilizadas

* ROS (Robot Operating System)
* Gazebo (simulação)
* RViz (visualização)
* Python
* OpenCV (visão computacional)

---

## Estrutura do Projeto

* `perception_pkg`: processamento de imagem e detecção de vítimas
* `slam_pkg`: mapeamento e localização
* `navigation_pkg`: planejamento e controle
* `simulation_pkg`: ambiente simulado no Gazebo

---

## Como Executar

1. Inicializar o workspace ROS
2. Rodar o ambiente de simulação no Gazebo
3. Executar os nós de SLAM
4. Iniciar o sistema de navegação
5. Executar o módulo de percepção

---

## Equipe e Responsabilidades

* Integrante 1: SLAM
* Integrante 2: Navegação
* Integrante 3: Visão Computacional
* Integrante 4: Integração ROS e Simulação

---

## Cronograma

O projeto segue três marcos principais:

* Milestone 1: Proposta do projeto
* Milestone 2: Implementação parcial
* Milestone 3: Entrega final e validação

---

## Riscos

* Falhas no SLAM
* Dificuldades na detecção de imagens
* Integração entre módulos

---

## Critérios de Sucesso

* Navegação autônoma funcional
* Mapeamento correto do ambiente
* Detecção de vítimas
* Integração completa do sistema

---
