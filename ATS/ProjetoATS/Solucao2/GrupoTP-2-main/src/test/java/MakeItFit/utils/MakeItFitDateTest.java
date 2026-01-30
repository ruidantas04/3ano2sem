package MakeItFit.utils;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

public class MakeItFitDateTest {

    @Test
    public void testDefaultConstructor() {
        MakeItFitDate date = new MakeItFitDate();
        assertNotNull(date);
    }

    @Test
    public void testOf() {
        MakeItFitDate date = MakeItFitDate.of(2024, 6, 1);
        assertEquals(1, date.getDayOfMonth());
        assertEquals(6, date.getMonth());
        assertEquals(2024, date.getYear());
    }

    @Test
    public void testFromString_Valid() {
        MakeItFitDate date = MakeItFitDate.fromString("01/06/2024");
        assertEquals("01/06/2024", date.toString());
    }

    @Test
    public void testFromString_InvalidFormat() {
        assertThrows(IllegalArgumentException.class, () -> MakeItFitDate.fromString("2024-06-01"));
        assertThrows(IllegalArgumentException.class, () -> MakeItFitDate.fromString("01/06"));
    }

    @Test
    public void testFromString_NonNumeric() {
        assertThrows(IllegalArgumentException.class, () -> MakeItFitDate.fromString("aa/bb/cccc"));
    }

    @Test
    public void testGetters() {
        MakeItFitDate date = MakeItFitDate.of(2024, 6, 2);
        assertEquals(2, date.getDayOfMonth());
        assertEquals(6, date.getMonth());
        assertEquals(2024, date.getYear());
        assertEquals(LocalDate.of(2024, 6, 2), date.getDate());
    }

    @Test
    public void testDayOfWeek() {
        MakeItFitDate date = MakeItFitDate.of(2024, 6, 3); // Monday
        assertEquals(1, date.getDayOfWeek());
    }

    @Test
    public void testPlusDays() {
        MakeItFitDate date = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate newDate = date.plusDays(5);
        assertEquals("06/06/2024", newDate.toString());
    }

    @Test
    public void testDistance() {
        MakeItFitDate d1 = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate d2 = MakeItFitDate.of(2024, 6, 10);
        assertEquals(9, d1.distance(d2));
        assertEquals(9, d2.distance(d1));
    }

    @Test
    public void testComparisonMethods() {
        MakeItFitDate d1 = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate d2 = MakeItFitDate.of(2024, 6, 10);

        assertTrue(d1.isBefore(d2));
        assertTrue(d2.isAfter(d1));
        assertTrue(d1.isBeforeOrSame(d2));
        assertTrue(d2.isAfterOrSame(d1));
        assertTrue(d1.isBeforeOrSame(d1));
        assertTrue(d1.isAfterOrSame(d1));
    }

    @Test
    public void testEqualsAndCompareTo() {
        MakeItFitDate d1 = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate d2 = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate d3 = MakeItFitDate.of(2024, 6, 2);

        assertEquals(d1, d2);
        assertNotEquals(d1, d3);
        assertEquals(0, d1.compareTo(d2));
        assertTrue(d1.compareTo(d3) < 0);
        assertTrue(d3.compareTo(d1) > 0);
    }

    @Test
    public void testToString() {
        MakeItFitDate date = MakeItFitDate.of(2024, 6, 1);
        assertEquals("01/06/2024", date.toString());
    }

    @Test
    public void testClone() {
        MakeItFitDate original = MakeItFitDate.of(2024, 6, 1);
        MakeItFitDate clone = original.clone();

        assertNotSame(original, clone);
        assertEquals(original, clone);
        assertEquals(original.toString(), clone.toString());
    }
}
