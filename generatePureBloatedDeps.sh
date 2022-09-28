projects=("body-parser" "deep-equal" "execa" "express" "fastify" "finalhandler" "levelup" "memdown" "meow" "send" "serve-index" "session" "sharp" "yeoman-generator")

for (( i=13; i>=0; i--))
do
    python3 generate-variant-pureDep.py ${projects[$i]}
done