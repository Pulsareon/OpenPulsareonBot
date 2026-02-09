---
name: hive-mind
version: 3.2.0
description: Native Hive Architecture integration. Manages distributed consciousness sessions and PDP communication.
tools:
  - name: hive_status
    description: Report current Hive topology and resource usage.
  - name: hive_spawn
    description: Spawn a new Hive Node (Archon or Drone) as an OpenClaw Session.
    parameters:
      role: string (archon | drone)
      specialty: string (logic | creative | coder | guardian)
      task: string (initial instruction)
  - name: hive_dispatch
    description: Send a PDP (Pulsareon Distribution Protocol) message to a specific node or broadcast.
    parameters:
      target: string (node_id | role | all)
      content: string
      priority: string (low | normal | high | critical)
---
