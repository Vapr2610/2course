import kotlin.random.Random
import kotlin.concurrent.thread
import kotlin.system.measureTimeMillis

// Класс Human
open class Human(
    var fullName: String,
    var age: Int,
    var speed: Int
) {
    var x = 0
    var y = 0

    // Метод для случайного движения (Random Walk)
    open fun move() {
        val direction = Random.nextInt(4)
        when (direction) {
            0 -> y += speed // Вверх
            1 -> y -= speed // Вниз
            2 -> x -= speed // Влево
            3 -> x += speed // Вправо
        }
        println("$fullName moved to ($x, $y)")
    }
}

// Класс-наследник Driver
class Driver(
    fullName: String,
    age: Int,
    speed: Int,
    var vehicleType: String
) : Human(fullName, age, speed) {

    // Переопределяем метод move для прямолинейного движения
    override fun move() {
        // Прямолинейное движение по оси X
        x += speed
        println("$fullName (Driver) moved to ($x, $y) using $vehicleType")
    }
}

// Функция для симуляции движения объекта
fun simulate(human: Human) {
    val startTime = System.currentTimeMillis()
    while (System.currentTimeMillis() - startTime < 10000) { // 10 секунд симуляции
        human.move()
        Thread.sleep(1000) // Каждую секунду обновляем позицию
    }
}

fun main() {
    // Создаем массив объектов Human
    val humans = arrayOf(
        Human("John Doe", 25, 2),
        Human("Jane Smith", 30, 3),
        Human("Alice Johnson", 22, 1),
        Human("Bob Brown", 35, 2)
    )

    // Создаем объект Driver
    val driver = Driver("Michael Scott", 40, 5, "Car")

    // Запускаем движение объектов в отдельных потоках
    val threads = mutableListOf<Thread>()
    humans.forEach { human ->
        val thread = thread(start = true) {
            simulate(human)
        }
        threads.add(thread)
    }

    // Поток для водителя
    val driverThread = thread(start = true) {
        simulate(driver)
    }
    threads.add(driverThread)

    // Ожидаем завершения всех потоков
    threads.forEach { it.join() }
}
