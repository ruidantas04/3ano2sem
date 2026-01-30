package MakeItFit.users;

import MakeItFit.activities.Activity;
import MakeItFit.activities.implementation.PushUp;
import MakeItFit.activities.implementation.Running;
import MakeItFit.activities.implementation.Trail;
import MakeItFit.exceptions.*;
import MakeItFit.users.types.Professional;
import MakeItFit.utils.MakeItFitDate;

import org.junit.jupiter.api.Test;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * The tests for the UserManager class.
 *
 * @version (11052024)
 */
public class UserManagerTest {

    @Test
    public void testConstructor() {
        UserManager userManager = new UserManager();
        assertNotNull(userManager);
    }

    @Test
    public void testCreateUserValidInputs() {
        UserManager userManager = new UserManager();
        User user = userManager.createUser("José Fernandes", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "josefernandes@mail.com", 7, "Professional");

        assertNotNull(user);
        assertEquals("José Fernandes", user.getName());
        assertEquals(45, user.getAge());
        assertEquals(Gender.Male, user.getGender());
        assertEquals(75, user.getWeight());
        assertEquals(175, user.getHeight());
        assertEquals(67, user.getBpm());
        assertEquals(6, user.getLevel());
        assertEquals("Braga", user.getAddress());
        assertEquals("990 000 000", user.getPhone());
        assertEquals("josefernandes@mail.com", user.getEmail());
    }

    @Test
    public void testCreateUserInvalidInputs() {
        UserManager um = new UserManager();
        assertThrows(IllegalArgumentException.class, () -> um.createUser(null, 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
        assertThrows(IllegalArgumentException.class, () -> um.createUser("José", -1, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
        assertThrows(IllegalArgumentException.class, () -> um.createUser("José", 45, Gender.Male, -75, 175, 67, 6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
        assertThrows(IllegalArgumentException.class, () -> um.createUser("José", 45, Gender.Male, 75, -175, 67, 6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
        assertThrows(IllegalArgumentException.class, () -> um.createUser("José", 45, Gender.Male, 75, 175, -67, 6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
        assertThrows(IllegalArgumentException.class, () -> um.createUser("José", 45, Gender.Male, 75, 175, 67, -6,
                "Braga", "990 000 000", "mail@mail.com", 7, "Professional"));
    }

    @Test
    public void testCreateUserInvalidType() {
        UserManager um = new UserManager();
        assertThrows(InvalidTypeException.class, () -> {
            um.createUser("José", 30, Gender.Male, 70, 175, 65, 3, "Rua", "999999999", "jose@mail.com", 2, "InvalidType");
        });
    }

    @Test
    public void testInsertUserValid() {
        UserManager um = new UserManager();
        User user = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");
        um.insertUser(user);
        assertNotNull(um.getUserByCode(user.getCode()));
    }

    @Test
    public void testInsertUserDuplicateEmail() {
        UserManager um = new UserManager();
        User user1 = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");
        um.insertUser(user1);

        User user2 = um.createUser("António", 25, Gender.Male, 95, 198, 72, 9,
                "Lisboa", "999999999", "jose@mail.com", 7, "Professional");

        assertThrows(ExistingEntityConflictException.class, () -> um.insertUser(user2));
    }

    @Test
    public void testRemoveUserByCodeValid() {
        UserManager um = new UserManager();
        User user = um.createUser("Ana", 28, Gender.Female, 60, 165, 70, 5,
                "Rua", "000000000", "ana@mail.com", 3, "Amateur");
        um.insertUser(user);
        um.removeUserByCode(user.getCode());

        assertThrows(EntityDoesNotExistException.class, () -> um.getUserByCode(user.getCode()));
    }

    @Test
    public void testRemoveUserByCodeInvalid() {
        UserManager um = new UserManager();
        assertThrows(EntityDoesNotExistException.class, () -> um.removeUserByCode(UUID.randomUUID()));
    }

    @Test
    public void testRemoveUserByEmailValid() {
        UserManager um = new UserManager();
        User user = um.createUser("Ana", 28, Gender.Female, 60, 165, 70, 5,
                "Rua", "000000000", "ana@mail.com", 3, "Amateur");
        um.insertUser(user);
        um.removeUserByEmail("ana@mail.com");

        assertThrows(EntityDoesNotExistException.class, () -> um.getUserByEmail("ana@mail.com"));
    }

    @Test
    public void testRemoveUserByEmailInvalid() {
        UserManager um = new UserManager();
        assertThrows(EntityDoesNotExistException.class, () -> um.removeUserByEmail("naoexiste@mail.com"));
    }

    @Test
    public void testExistsUserWithEmail() {
        UserManager um = new UserManager();
        User user = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");
        um.insertUser(user);

        assertTrue(um.existsUserWithEmail("jose@mail.com"));
        assertFalse(um.existsUserWithEmail("outro@mail.com"));
    }

    @Test
    public void testGetUserByEmailAndCode() {
        UserManager um = new UserManager();
        User user = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");
        um.insertUser(user);

        assertNotNull(um.getUserByEmail("jose@mail.com"));
        assertNotNull(um.getUserByCode(user.getCode()));
    }

    @Test
    public void testUpdateUserValid() {
        UserManager um = new UserManager();
        User user = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");
        um.insertUser(user);

        user.setAge(50);
        user.setLevel(10);
        um.updateUser(user);

        User updated = um.getUserByCode(user.getCode());
        assertEquals(50, updated.getAge());
        assertEquals(10, updated.getLevel());
    }

    @Test
    public void testUpdateUserInvalid() {
        UserManager um = new UserManager();
        User user = um.createUser("José", 45, Gender.Male, 75, 175, 67, 6,
                "Braga", "990 000 000", "jose@mail.com", 7, "Professional");

        assertThrows(EntityDoesNotExistException.class, () -> um.updateUser(user));
    }

    @Test
    public void testGetAllUsersEmptyAndNonEmpty() {
        UserManager um = new UserManager();
        assertTrue(um.getAllUsers().isEmpty());

        User user1 = um.createUser("User1", 30, Gender.Male, 70, 180, 65, 5,
                "Rua", "111", "u1@mail.com", 2, "Amateur");
        User user2 = um.createUser("User2", 32, Gender.Female, 60, 165, 70, 4,
                "Rua", "222", "u2@mail.com", 3, "Occasional");

        um.insertUser(user1);
        um.insertUser(user2);

        List<User> allUsers = um.getAllUsers();
        assertEquals(2, allUsers.size());
        assertTrue(allUsers.contains(user1));
        assertTrue(allUsers.contains(user2));
    }

    @Test
    public void testGetActivitiesFromUserValidAndInvalid() throws Exception {
        UserManager um = new UserManager();
        User user = um.createUser("Bruno", 33, Gender.Male, 80, 180, 65, 4,
                "Rua", "111111111", "bruno@mail.com", 2, "Occasional");
        um.insertUser(user);

        assertEquals(0, um.getActivitiesFromUser("bruno@mail.com").size());

        assertThrows(EntityDoesNotExistException.class, () -> um.getActivitiesFromUser("naoexiste@mail.com"));
    }

    @Test
    public void testAddAndRemoveActivityFromUser() {
        UserManager um = new UserManager();
        User user = um.createUser("Sara", 29, Gender.Female, 65, 170, 65, 4,
                "Rua", "321", "sara@mail.com", 3, "Occasional");
        um.insertUser(user);

        Activity activity = new PushUp(user.getCode(), MakeItFitDate.of(2024, 6, 2),
                20, "Treino", "PushUp", 15, 3);
        um.addActivityToUser("sara@mail.com", activity);

        assertEquals(1, user.getListActivities().size());

        um.removeActivityFromUser("sara@mail.com", activity.getCode());
        assertEquals(0, user.getListActivities().size());
    }

    @Test
    public void testAddActivitiesToUser() {
        UserManager um = new UserManager();
        User user = um.createUser("Mário", 40, Gender.Male, 85, 178, 72, 6,
                "Rua", "999", "mario@mail.com", 1, "Professional");
        um.insertUser(user);

        List<Activity> activities = Arrays.asList(
                new Running(user.getCode(), MakeItFitDate.of(2024, 6, 3), 25, "Run", "Running", 2000, 9),
                new Trail(user.getCode(), MakeItFitDate.of(2024, 6, 4), 45, "Mountain", "Trail", 3000, 300, 200, 2)
        );

        um.addActivitiesToUser(user.getCode(), activities);
        assertEquals(2, user.getListActivities().size());
    }

    @Test
    public void testUpdateSystem() {
        UserManager um = new UserManager();
        Professional user = new Professional("Luís", 37, Gender.Male, 78, 176, 68, 5,
                "Rua", "111", "luis@mail.com", 3);
        um.insertUser(user);

        Activity activity = new PushUp(user.getCode(), MakeItFitDate.of(2024, 4, 1),
                15, "Push", "PushUp", 12, 2);
        user.addActivity(activity);

        assertEquals("No specialization", user.getSpecialization());

        um.updateSystem();

        assertEquals("PushUp", user.getSpecialization());
    }
}
