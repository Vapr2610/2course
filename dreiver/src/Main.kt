import kotlin.random.Random

fun main() {
    val people = Array(8) {
        Human("Human ${it + 1}", Random.nextInt(18, 60), Random.nextDouble(1.0, 5.0))
        //Driver("Driver ${it + 1}", Random.nextInt(18, 60), Random.nextDouble(60.0, 100.0))
    }
    val peopled = Array(8){
        Driver("Driver ${it + 1}", Random.nextInt(18, 60), Random.nextDouble(10.0, 30.0))
    }

    /*val people = Array<Any>(16)
    {
        Human("Human ${it + 1}", Random.nextInt(18, 60), Random.nextDouble(1.0, 5.0))
        Driver("Driver ${it + 1}", Random.nextInt(18, 60), Random.nextDouble(60.0, 100.0))
    }*/

    val simulationTime = 5.0
    val step = 1.0

    println("Начало симуляции движения (${people.size+peopled.size} объектов)\n")

    val threads = mutableListOf<Thread>()

    for (person in people ) {
        val t = Thread {
            var time = 0.0
            while (time <= simulationTime) {
                person.move(step)
                //persond.move(step)
                println(" ${person.getName()} → (%.2f, %.2f)".format(person.x, person.y))
                //println(" ${persond.getName()} → (%.2f, %.2f)".format(persond.x, persond.y))
                time += step
                Thread.sleep((300..900).random().toLong())
            }
        }
            t.name = person.getName()
            //t.name = persond.getName()
        threads.add(t)
    }

    for (person in peopled ) {
        val t = Thread {
            var time = 0.0
            while (time <= simulationTime) {
                person.move(step)
                println(" ${person.getName()} → (%.2f, %.2f)".format(person.x, person.y))
                time += step
                Thread.sleep((300..900).random().toLong())
            }
        }
        t.name = person.getName()
        threads.add(t)
    }

    // запускаем все потоки
    threads.forEach { it.start() }
    threads.forEach { it.join() }

    println("\nСимуляция завершена!")
    println("\nФинальные позиции:")

    println("_".repeat(60))
    for (person in people) {
        println("%-40s (%.2f; %.2f)".format(person.getName(), person.x, person.y))
    }
    println("=".repeat(60))
    for (person in peopled) {
        println("%-40s (%.2f; %.2f)".format(person.getName(), person.x, person.y))
    }
    println("_".repeat(60))
}
