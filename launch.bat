@echo off
REM -------------------------------
REM Script pour exécuter le chatbot médical Neo4j + Gemini
REM Charge les variables d'environnement depuis le fichier .env
REM -------------------------------

REM 1. Activer l'environnement Python
call venv\Scripts\activate.bat

REM 2. Charger le fichier .env
for /f "tokens=1,2 delims==" %%A in (.env) do set %%A=%%B

REM 3. Construire le graphe médical dans Neo4j
echo Création du graphe médical...
python graph\build_graph.py
if %ERRORLEVEL% neq 0 (
    echo Erreur lors de la construction du graphe.
    pause
    exit /b %ERRORLEVEL%
)

REM 4. Lancer le chatbot interactif
echo Lancement du chatbot médical...
python langchain_pipeline\chatbot_gemini.py
if %ERRORLEVEL% neq 0 (
    echo Erreur lors du lancement du chatbot.
    pause
    exit /b %ERRORLEVEL%
)

REM 5. Fin
echo Chatbot terminé.
pause
