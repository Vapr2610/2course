class Driver(name: String, age: Int, speed: Double)  : Human(name, age, speed) {

    override fun move(dt: Double) {
        x += speed * dt // движение по оси X
    }
}