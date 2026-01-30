import org.junit.Test;
import static org.junit.Assert.*;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

public class TestLift {

    @Test(timeout = 4000)
    public void testInitialFloor() {
        Lift lift = new Lift(10);
        assertEquals(0, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testInitialCapacity() {
        Lift lift = new Lift(10);
        assertEquals(10, lift.getCapacity());
    }

    @Test(timeout = 4000)
    public void testAddRiders() {
        Lift lift = new Lift(10);
        lift.addRiders(5);
        assertEquals(5, lift.getNumRiders());
    }

    @Test(timeout = 4000)
    public void testGoUp() {
        Lift lift = new Lift(10);
        lift.goUp();
        assertEquals(1, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testGoDown() {
        Lift lift = new Lift(10);
        lift.goUp();
        lift.goDown();
        assertEquals(0, lift.getCurrentFloor());
    }


    public void testIsFull() {
        Lift lift = new Lift(10);
        lift.addRiders(10);
        assertTrue(lift.isFull());
    }

    public void testCall() {
        Lift lift = new Lift(10);
        lift.call(5);
        assertEquals(5, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testInitialFloor() {
        Lift lift = new Lift(10);
        assertEquals(0, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testInitialCapacity() {
        Lift lift = new Lift(10);
        assertEquals(10, lift.getCapacity());
    }

    @Test(timeout = 4000)
    public void testAddRiders() {
        Lift lift = new Lift(10);
        lift.addRiders(5);
        assertEquals(5, lift.getNumRiders());
        lift.addRiders(6); // Trying to add 6 more riders (total should be 10)
        assertEquals(10, lift.getNumRiders()); // The lift should be full now
    }

    @Test(timeout = 4000)
    public void testGoUp() {
        Lift lift = new Lift(10);
        lift.goUp();
        assertEquals(1, lift.getCurrentFloor());
        lift.goUp();
        assertEquals(2, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testGoDown() {
        Lift lift = new Lift(10);
        lift.goUp();
        lift.goUp();
        lift.goDown();
        assertEquals(1, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testIsFull() {
        Lift lift = new Lift(10);
        lift.addRiders(10);
        assertTrue(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testCall() {
        Lift lift = new Lift(10);
        lift.call(5);
        assertEquals(5, lift.getCurrentFloor());
    }

    @Test(timeout = 4000)
    public void testInitialFloor() {
        Lift lift = new Lift(10);
        assertEquals(0, lift.getCurrentFloor()); 
    }

    @Test(timeout = 4000)
    public void testAddRidersOverflow() {
        Lift lift = new Lift(10);
        lift.addRiders(10); /
        assertEquals(10, lift.getNumRiders()); // O elevador deve estar cheio
        lift.addRiders(5); // Tentando adicionar mais 5 passageiros (excedendo a capacidade)
        assertEquals(10, lift.getNumRiders()); // O elevador não deve aceitar mais do que 10 passageiros
    }

    @Test(timeout = 4000)
    public void testAddRidersNotExceedingCapacity() {
        Lift lift = new Lift(10);
        lift.addRiders(5); // Adicionando 5 passageiros
        assertEquals(5, lift.getNumRiders()); // O elevador deve ter 5 passageiros
        lift.addRiders(4); // Adicionando 4 passageiros (não excede a capacidade)
        assertEquals(9, lift.getNumRiders()); // O elevador deve ter 9 passageiros no total
    }

    @Test(timeout = 4000)
    public void testGoUp() {
        Lift lift = new Lift(10);
        lift.goUp(); // Mover para o andar 1
        assertEquals(1, lift.getCurrentFloor()); // O elevador deve estar no andar 1
        lift.goUp(); // Mover para o andar 2
        assertEquals(2, lift.getCurrentFloor()); // O elevador deve estar no andar 2
    }

    @Test(timeout = 4000)
    public void testGoDown() {
        Lift lift = new Lift(10);
        lift.goUp(); // Mover para o andar 1
        lift.goDown(); // Mover de volta para o andar 0
        assertEquals(0, lift.getCurrentFloor()); // O elevador deve estar no andar 0
    }

    @Test(timeout = 4000)
    public void testCall() {
        Lift lift = new Lift(10);
        lift.call(5); // Chamar o elevador para o andar 5
        assertEquals(5, lift.getCurrentFloor()); // O elevador deve estar no andar 5
    }

    @Test(timeout = 4000)
    public void testIsFullWhenEmpty() {
        Lift lift = new Lift(10);
        assertFalse(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullWhenFull() {
        Lift lift = new Lift(10);
        lift.addRiders(10);
        assertTrue(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullWhenNotFull() {
        Lift lift = new Lift(10);
        lift.addRiders(5);
        assertFalse(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullAfterOverCapacityAttempt() {
        Lift lift = new Lift(10);
        lift.addRiders(10);
        lift.addRiders(5);
        assertTrue(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullWhenExactlyAtCapacity() {
        Lift lift = new Lift(10);
        lift.addRiders(10);
        assertTrue(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullAfterAddingLessThanCapacity() {
        Lift lift = new Lift(10);
        lift.addRiders(8);
        assertFalse(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullWithZeroCapacity() {
        Lift lift = new Lift(0);
        assertTrue(lift.isFull());
    }

    @Test(timeout = 4000)
    public void testIsFullWithZeroRiders() {
        Lift lift = new Lift(10);
        lift.addRiders(0);
        assertFalse(lift.isFull());
    }
    @Test
    public void testCall() {
        // Criar um elevador com 5 andares
        Lift lift = new Lift(5);

        // Caso o elevador esteja no andar 0 e chamemos o andar 3, ele deve subir
        lift.call(3);
        assertEquals(3, lift.getCurrentFloor(), "O elevador deve estar no andar 3.");

        // Agora, caso o elevador esteja no andar 3 e chamemos o andar 1, ele deve descer
        lift.call(1);
        assertEquals(1, lift.getCurrentFloor(), "O elevador deve estar no andar 1.");

        // Caso o elevador esteja no andar 1 e chamemos o andar 5, ele deve subir até o último andar
        lift.call(5);
        assertEquals(5, lift.getCurrentFloor(), "O elevador deve estar no andar 5.");

        // Caso o elevador esteja no andar 5 e chamemos o andar 0, ele deve descer até o primeiro andar
        lift.call(0);
        assertEquals(0, lift.getCurrentFloor(), "O elevador deve estar no andar 0.");
    }
}

}

}


