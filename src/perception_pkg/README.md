# perception_pkg

Pacote ROS responsável por percepção visual em tempo real utilizando **MediaPipe + OpenCV**, com detecção de partes do corpo humano e estimativa de número de pessoas.

---

## 📌 Funcionalidades

O nó `perception_node` realiza:

- Detecção de **rostos** (MediaPipe Face Detection)
- Detecção de **mãos** (MediaPipe Hands)
- Estimativa de **braços, pernas e tronco** (MediaPipe Pose)
- Contagem de:
  - Faces
  - Mãos
  - Braços
  - Pernas
  - Troncos
  - Pessoas estimadas
- Geração de bounding boxes na imagem
- Publicação de imagem processada no ROS
- Estimativa simples de presença humana

---

## 📡 Tópicos ROS

### 📥 Entrada
| Tópico | Tipo | Descrição |
|--------|------|-----------|
| `/usb_cam/image_raw` | `sensor_msgs/Image` | Stream da câmera |

---

### 📤 Saída (contagens)
| Tópico | Tipo | Descrição |
|--------|------|-----------|
| `/perception/face_count` | `std_msgs/Int32` | Número de faces detectadas |
| `/perception/hand_count` | `std_msgs/Int32` | Número de mãos detectadas |
| `/perception/arm_count` | `std_msgs/Int32` | Número de braços detectados |
| `/perception/leg_count` | `std_msgs/Int32` | Número de pernas detectadas |
| `/perception/torso_count` | `std_msgs/Int32` | Número de troncos detectados |
| `/perception/person_count` | `std_msgs/Int32` | Estimativa de número de pessoas |
| `/perception/human_detected` | `std_msgs/Bool` | Presença de humano |

---

### 📤 Saída (imagem)
| Tópico | Tipo | Descrição |
|--------|------|-----------|
| `/perception/image` | `sensor_msgs/Image` | Imagem processada com bounding boxes |

---

## 🧠 Lógica de Estimativa de Pessoas

A estimativa de pessoas é baseada em heurísticas:

- Se houver faces:
  - `person_count = max(faces, mãos/2)`
- Se houver mãos apenas:
  - `person_count = mãos / 2`
- Caso contrário:
  - Presença de torso, braços ou pernas indica pelo menos 1 pessoa

---

## 🎨 Detecções visuais

Na imagem publicada:

- 🔵 FACE → bounding box azul
- 🟣 HAND → roxo
- 🟡 TORSO → amarelo
- 🟢 ARM → verde
- 🟨 LEG → amarelo claro

---

## ⚙️ Dependências

### ROS
- rospy
- std_msgs
- sensor_msgs
- cv_bridge

### Python
- OpenCV
- MediaPipe