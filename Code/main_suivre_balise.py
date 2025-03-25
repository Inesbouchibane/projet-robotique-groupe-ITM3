




















 running = True
    while running:
        strategie.step()
        if strategie.running:  # Ne refresh que si la stratégie est active
            robot.refresh(TIC_SIMULATION)
            affichage.mettre_a_jour(robot)
            
            
        # Gestion des événements pour quitter
        action = affichage.handle_events(adaptateur)
        if action == "quit":
            strategie.stop()
            running = False

        sleep(TIC_SIMULATION)

    affichage.attendre_fermeture()

