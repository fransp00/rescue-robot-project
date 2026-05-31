# teleop_p3dx

Pacote ROS responsável pelo controle manual de um robô diferencial utilizando teclado (WASD), com **camada de segurança baseada em LiDAR**, impedindo colisões frontais em tempo real.

---

## 📌 Funcionalidades

O script `teleop_keyboard.py` realiza:

- Leitura do teclado em tempo real (W, A, S, D)
- Controle de velocidade linear e angular
- Publicação de comandos de movimento no ROS
- Leitura do sensor LiDAR (LaserScan)
- Detecção de obstáculos à frente
- Bloqueio automático de movimento para frente quando há risco de colisão
- Permissão de rotação e ré mesmo com obstáculo
- Parada automática ao encerrar o programa

---

## 📡 Tópicos ROS

### 📥 Entrada

| Tópico | Tipo | Descrição |
|--------|------|-----------|
| `/p3dx/laser/scan` | `sensor_msgs/LaserScan` | Dados do sensor LiDAR frontal |

---

### 📤 Saída

| Tópico | Tipo | Descrição |
|--------|------|-----------|
| `/p3dx/cmd_vel` | `geometry_msgs/Twist` | Comando de velocidade enviado ao robô |

---

## 🧠 Lógica de Segurança

O sistema analisa os dados do LiDAR na região frontal do robô:

- Seleciona uma janela central do LaserScan (aprox. ±15°)
- Remove leituras inválidas (`inf` e `nan`)
- Calcula a menor distância detectada

### Regras de segurança:

- Se `distância < 0.5 m`:
  - O movimento para frente (`W`) é bloqueado
- Se `distância ≥ 0.5 m`:
  - Movimento permitido normalmente
- Movimentos de ré e rotação não são bloqueados

---

## 🎮 Controle do teclado

| Tecla | Ação |
|------|------|
| `w` | Move para frente |
| `s` | Move para trás |
| `a` | Gira para esquerda |
| `d` | Gira para direita |
| `q` | Encerra o nó |

---

## ⚙️ Parâmetros principais

| Parâmetro | Valor | Descrição |
|----------|------|-----------|
| linear_speed | 0.5 m/s | Velocidade linear do robô |
| angular_speed | 1.0 rad/s | Velocidade angular |
| safety_distance | 0.5 m | Distância mínima para evitar colisão |

---

## 🧠 Comportamento do sistema

- O robô só avança se não houver obstáculo frontal
- O sistema não permite colisões frontais
- O controle é em tempo real
- A leitura do teclado é não bloqueante
- O nó roda continuamente a 20 Hz

---

## ⚙️ Dependências

### ROS
- rospy
- geometry_msgs
- sensor_msgs