


f = open("story.txt", "a")
f.write("One fine day, a cat was walking in the park. It was a sunny day and the birds were chirping. The cat was enjoying the weather and the beautiful surroundings.")

f.close()
f = open("story.txt", "r")
print(f.read())
f.close()