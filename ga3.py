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
    courses = cur.fetchall()
    print(courses)

    # Fetch slot data
    cur.execute("SELECT slot FROM slots")
    timeslots = list(set([row[0] for row in cur.fetchall()]))
    print(timeslots)

    # Fetch only faculty data
    cur.execute("SELECT Faculty_ID FROM faculty_id")
    facultyID = [row[0] for row in cur.fetchall()]
    print(facultyID)

    # Fetch faculty-course assignment data
    cur.execute("SELECT Course_Number, Faculty FROM faculty_course")
    faculties = cur.fetchall()

    # Transform faculty data if a course has multiple faculties
    transformed_data = []
    for course, faculty in faculties:
        if ',' in faculty:
            transformed_data.append((course, faculty.split(',')))
        else:
            transformed_data.append((course, [faculty]))

    faculties = transformed_data
    print(faculties)

    cur.close()
    return courses, timeslots, faculties, facultyID

# Create a gene (course with timeslot and faculty)
def create_gene(course, timeslot, faculty):
    return (course, timeslot, faculty)

# Function to create a chromosome (schedule)
def create_chromosome(courses, timeslots, faculties):
    chromosome = []
    for course_sem, course_num in courses:
        available_faculties = [faculty for cnum, faculty in faculties if cnum == course_num]
        if available_faculties:
            timeslot = random.choice(timeslots)
            faculty = random.choice(available_faculties[0])
            gene = create_gene((course_sem, course_num), timeslot, faculty)
            chromosome.append(gene)
    return chromosome

# Function to count conflicts in a chromosome
def count_conflicts(courses, chromosome):
    conflicts = 0
    num_genes = len(chromosome)
    
    for i in range(num_genes):
        gene1 = chromosome[i]
        sem1 = next((sem for sem, course in courses if course == gene1[0][1]), None)

        for j in range(i + 1, num_genes):
            gene2 = chromosome[j]
            sem2 = next((sem for sem, course in courses if course == gene2[0][1]), None)

            # Check for conflicts
            if sem1 == sem2:
                if gene1[1] == gene2[1] or gene1[2] == gene2[2]:
                    conflicts += 1
            else:
                if gene1[1] == gene2[1] and gene1[2] == gene2[2]:
                    conflicts += 1
    
    return conflicts

# Function to calculate the fitness of an individual
def calculate_fitness(num_conflicts):
    return 1 / (1 + num_conflicts)

def create_individual(courses, timeslots, faculties, generation):
    chromosome = create_chromosome(courses, timeslots, faculties)
    num_conflicts = count_conflicts(courses, chromosome)
    fitness = calculate_fitness(num_conflicts)
    return {
        "chromosome": chromosome,
        "fitness": fitness,
        "num_conflicts": num_conflicts,
        "generation": generation
    }

# Function to create an initial population
def create_population(pop_size, courses, timeslots, faculties):
    return [create_individual(courses, timeslots, faculties, generation=0) for _ in range(pop_size)]

# Function to order the population by fitness
def order_population(population):
    return sorted(population, key=lambda x: x["fitness"], reverse=True)

# Function to sum evaluations (for selection)
def sum_evaluations(population):
    return sum(individual["fitness"] for individual in population)

# Function to perform selection (roulette wheel selection)
def select_individuals(population):
    max_fitness = sum_evaluations(population)
    pick = random.uniform(0, max_fitness)
    current = 0
    for individual in population:
        current += individual["fitness"]
        if current > pick:
            return individual

# Crossover between two parents
def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1['chromosome']) - 1)
    offspring1 = parent1['chromosome'][:crossover_point] + parent2['chromosome'][crossover_point:]
    offspring2 = parent2['chromosome'][:crossover_point] + parent1['chromosome'][crossover_point:]
    return offspring1, offspring2

# Mutation function
def mutate(chromosome, timeslots, faculties, mutation_rate=0.01):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            course = chromosome[i][0]
            chromosome[i] = (
                course,
                random.choice(timeslots),
                random.choice([fac[1] for fac in faculties if fac[0] == course[1]][0])
            )
    return chromosome

# Visualize the best individual
def visualize_generation(best_individual, generation):
    print(f"Best individual in generation {generation}:")
    print(f"Fitness: {best_individual['fitness']}")
    print(f"Number of conflicts: {best_individual['num_conflicts']}")
    for gene in best_individual['chromosome']:
        print(f"Course: {gene[0]}, Timeslot: {gene[1]}, Faculty: {gene[2]}")
    print("-" * 40)

# Genetic algorithm main function
def genetic_algorithm(pop_size, generations, courses, timeslots, faculties):
    population = create_population(pop_size, courses, timeslots, faculties)
    
    for generation in range(generations):
        population = order_population(population)
        visualize_generation(population[0], generation)
        next_population = population[:pop_size // 2]

        while len(next_population) < pop_size:
            parent1 = select_individuals(population)
            parent2 = select_individuals(population)
            offspring1, offspring2 = crossover(parent1, parent2)
            next_population.append({
                "chromosome": mutate(offspring1, timeslots, faculties),
                "fitness": calculate_fitness(count_conflicts(courses, offspring1)),
                "num_conflicts": count_conflicts(courses, offspring1),
                "generation": generation + 1
            })
            next_population.append({
                "chromosome": mutate(offspring2, timeslots, faculties),
                "fitness": calculate_fitness(count_conflicts(courses, offspring2)),
                "num_conflicts": count_conflicts(courses, offspring2),
                "generation": generation + 1
            })

        population = next_population

    population = order_population(population)
    return population[0]

# Main function
def main():
    conn = connect_db()
    if not conn:
        return
    courses, timeslots, faculties, facultyID = fetch_data(conn)
    conn.close()

    best_individual = genetic_algorithm(pop_size=50, generations=100, courses=courses, timeslots=timeslots, faculties=faculties)
    
    print("Best solution found:")
    visualize_generation(best_individual, best_individual['generation'])

if __name__ == "__main__":
    main()
