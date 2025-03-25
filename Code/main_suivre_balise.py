




















 running = True
    while running:
        strategie.step()
        if strategie.running:  # Ne refresh que si la stratégie est active
            robot.refresh(TIC_SIMULATION)
            affichage.mettre_a_jour(robot)
