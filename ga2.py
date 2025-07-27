import random
import psycopg2

# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tt_project",
            user="postgres",
            password="ubaid"
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

# Fetch required data from the database
def fetch_data(conn):
    cur = conn.cursor()

    # Fetch course data
    cur.execute("SELECT Semester, Course_Number FROM course_structure")
    # semesters=[row[0] for row in cur.fetchall()]
    courses = [cur.fetchall()]
    # print(semesters)
    print(courses)
    print("\n")

    # Fetch timeslot data
    cur.execute("SELECT id FROM timeslots2")
    timeslots = [row[0] for row in cur.fetchall()]
    print(timeslots)
    print("\n")

    # Fetch faculty data
    cur.execute("SELECT Course_Number, Faculty FROM faculty_course")
    course_numbers=[row[0] for row in cur.fetchall()]
    print(course_numbers)
    faculties = [row[1] for row in cur.fetchall()]
    print(faculties)

    cur.close()
    return courses, timeslots, faculties

# Create the gene (individual course with timeslot and faculty)
def create_gene(courses, timeslots, faculties):
    course = random.choice(courses)
    timeslot = random.choice(timeslots)
    faculty = random.choice(faculties)
    return (course, timeslot, faculty)

# Create an initial population of timetables
def create_population(population_size, courses, timeslots, faculties):
    return [create_gene(courses, timeslots, faculties) for _ in range(population_size)]

# Fitness function: check for conflicts (faculty or timeslot overlaps)
def fitness_function(timetable):
    fitness = 0
    seen_timeslots = set()
    seen_faculty_times = {}

    for gene in timetable:
        course, timeslot, faculty = gene

        # Check for timeslot conflicts (same timeslot assigned to multiple courses)
        if timeslot in seen_timeslots:
            fitness -= 10
        else:
            seen_timeslots.add(timeslot)

        # Check for faculty conflicts (same faculty assigned to multiple courses in the same timeslot)
        if (faculty, timeslot) in seen_faculty_times:
            fitness -= 10
        else:
            seen_faculty_times[(faculty, timeslot)] = course

    return fitness

# Selection: select the top individuals based on fitness
def selection(population, fitnesses, num_parents):
    selected = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
    return [x[0] for x in selected[:num_parents]]

# Crossover: crossover between two parents to generate a child
def crossover(parent1, parent2):
    cut_point = random.randint(0, len(parent1) - 1)
    child = parent1[:cut_point] + parent2[cut_point:]
    return child

# Mutation: randomly mutate a gene in a child
def mutation(child, courses, timeslots, faculties, mutation_rate=0.01):
    if random.random() < mutation_rate:
        index = random.randint(0, len(child) - 1)
        child[index] = create_gene(courses, timeslots, faculties)
    return child

# Genetic Algorithm
def genetic_algorithm(conn, population_size=100, generations=50, mutation_rate=0.01):
    # Fetch data from the database
    courses, timeslots, faculties = fetch_data(conn)

    # Initialize the population
    population = [create_population(len(courses), courses, timeslots, faculties) for _ in range(population_size)]

    for generation in range(generations):
        # Calculate fitness for each individual in the population
        fitnesses = [fitness_function(timetable) for timetable in population]

        # Select the top individuals to be parents
        parents = selection(population, fitnesses, population_size // 2)

        # Create the next generation
        next_generation = []

        # Crossover and mutation
        while len(next_generation) < population_size:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = crossover(parent1, parent2)
            child = mutation(child, courses, timeslots, faculties, mutation_rate)
            next_generation.append(child)

        # Replace old population with the new generation
        population = next_generation

        # Print best fitness in the current generation
        best_fitness = max(fitnesses)
        print(f"Generation {generation}: Best fitness = {best_fitness}")

    # Return the best timetable (the one with the highest fitness)
    best_timetable = max(population, key=fitness_function)
    return best_timetable

# Display the best timetable
def display_best_timetable(best_timetable):
    print("\nBest Timetable:")
    for course, timeslot, faculty in best_timetable:
        print(f"Course: {course}, Timeslot: {timeslot}, Faculty: {faculty}")

def main():
    conn = connect_db()
    if conn is None:
        return

    # Run the genetic algorithm
    best_timetable = genetic_algorithm(conn)

    # Display the best timetable
    display_best_timetable(best_timetable)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
