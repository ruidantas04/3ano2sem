package MakeItFit.trainingPlan;

import static org.junit.jupiter.api.Assertions.*;

import MakeItFit.activities.implementation.PushUp;
import MakeItFit.exceptions.EntityDoesNotExistException;
import MakeItFit.trainingPlan.TrainingPlan;
import MakeItFit.utils.MakeItFitDate;
import org.junit.jupiter.api.Test;
import MakeItFit.trainingPlan.TrainingPlanManager;

import java.util.UUID;

/**
 * The tests for the TrainingPlanManager class.
 *
 * @author  Afonso Santos (a104276), Hélder Gomes (a104100) and Pedro Pereira (a104100)
 * @version (11052024)
 */
public class TrainingPlanManagerTest {

    /**
     * Tests the creation of TrainingPlanManager instances using different constructors.
     */
    @Test
    public void testCreateTrainingPlan() {
        UUID userCode = UUID.randomUUID();
        MakeItFitDate startDate = MakeItFitDate.of(2024, 4, 4);

        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan trainingPlan = manager.createTrainingPlan(userCode, startDate);

        assertNotNull(trainingPlan);
        assertEquals(userCode, trainingPlan.getUserCode());
        assertEquals(startDate, trainingPlan.getStartDate());
    }

    /**
     * Test the method createTrainingPlan with null inputs
     */
    @Test
    public void testCreateTrainingPlanWithNullInputs() {
        TrainingPlanManager manager = new TrainingPlanManager();
        assertThrows(IllegalArgumentException.class, () -> {
            manager.createTrainingPlan(null, MakeItFitDate.of(2024, 4, 4));
        });

        assertThrows(IllegalArgumentException.class, () -> {
            manager.createTrainingPlan(UUID.randomUUID(), null);
        });
    }

    /**
     * Test the method insertTrainingPlan with a null training plan
     */
    @Test
    public void testInsertTrainingPlanWithNullTrainingPlan() {
        TrainingPlanManager manager = new TrainingPlanManager();
        assertThrows(IllegalArgumentException.class, () -> {
            manager.insertTrainingPlan(null);
        });
    }

    /**
    * Test the method removeTrainingPlan with a valid training plan
    */
    @Test
    public void testRemoveTrainingPlan() {
        TrainingPlan trainingPlan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));
        TrainingPlanManager manager = new TrainingPlanManager();

        manager.insertTrainingPlan(trainingPlan);
        UUID code = trainingPlan.getCode(); // Usa o código real do plano inserido

        manager.removeTrainingPlan(code);

        assertThrows(IllegalArgumentException.class, () -> {
            manager.getTrainingPlan(code); // Espera falhar, pois foi removido
        });
    }


    /**
     * Test the method getAllTrainingPlans with a valid training plan
     */
    @Test
    public void testGetAllTrainingPlans() {
        TrainingPlan trainingPlan1 = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));
        TrainingPlan trainingPlan2 = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));

        TrainingPlanManager manager = new TrainingPlanManager();
        manager.insertTrainingPlan(trainingPlan1);
        manager.insertTrainingPlan(trainingPlan2);

        assertEquals(2, manager.getAllTrainingPlans().size());
    }

    @Test
    public void testConstructTrainingPlanByObjectivesValid() {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));

        TrainingPlan result = manager.constructTrainingPlanByObjectives(
                plan, 1.0f, false, 3, 2, 4, 100 // parâmetros típicos válidos
        );

        assertNotNull(result);
        assertFalse(result.getActivities().isEmpty());
    }

    @Test
    public void testConstructTrainingPlanByObjectivesWithInvalidParams() {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));

        assertThrows(IllegalArgumentException.class, () -> {
            manager.constructTrainingPlanByObjectives(plan, 1.0f, false, 4, 2, 4, 100); // maxActivitiesPerDay > 3
        });

        assertThrows(IllegalArgumentException.class, () -> {
            manager.constructTrainingPlanByObjectives(plan, 1.0f, false, 2, 2, 8, 100); // weeklyRecurrence > 7
        });

        assertThrows(IllegalArgumentException.class, () -> {
            manager.constructTrainingPlanByObjectives(plan, 1.0f, false, 2, 2, 4, -50); // caloricWaste < 0
        });
    }

    @Test
    public void testUpdateTrainingPlan() throws EntityDoesNotExistException {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));
        manager.insertTrainingPlan(plan);

        plan.setStartDate(MakeItFitDate.of(2024, 5, 1));
        manager.updateTrainingPlan(plan);

        assertEquals(MakeItFitDate.of(2024, 5, 1), manager.getTrainingPlan(plan.getCode()).getStartDate());
    }

    @Test
    public void testUpdateTrainingPlanNonExisting() {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));

        assertThrows(EntityDoesNotExistException.class, () -> {
            manager.updateTrainingPlan(plan);
        });
    }

    @Test
    public void testAddActivityToTrainingPlan() {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));
        manager.insertTrainingPlan(plan);

        PushUp pushUp = new PushUp(plan.getUserCode(), MakeItFitDate.of(2024, 4, 5), 20, "auto", "PushUp", 10, 3);
        manager.addActivity(plan.getCode(), 2, pushUp);

        assertEquals(1, manager.getTrainingPlan(plan.getCode()).getActivities().size());
    }

    @Test
    public void testRemoveActivityFromTrainingPlan() {
        TrainingPlanManager manager = new TrainingPlanManager();
        TrainingPlan plan = new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 4));
        manager.insertTrainingPlan(plan);

        PushUp pushUp = new PushUp(plan.getUserCode(), MakeItFitDate.of(2024, 4, 5), 20, "auto", "PushUp", 10, 3);
        plan.addActivity(2, pushUp);

        manager.removeActivity(plan.getCode(), pushUp.getCode());
        assertEquals(0, plan.getActivities().size());
    }

    @Test
    public void testGetTrainingPlansFromUser() {
        UUID userCode = UUID.randomUUID();
        TrainingPlanManager manager = new TrainingPlanManager();
        manager.insertTrainingPlan(new TrainingPlan(userCode, MakeItFitDate.of(2024, 4, 4)));
        manager.insertTrainingPlan(new TrainingPlan(userCode, MakeItFitDate.of(2024, 4, 5)));
        manager.insertTrainingPlan(new TrainingPlan(UUID.randomUUID(), MakeItFitDate.of(2024, 4, 6)));

        assertEquals(2, manager.getTrainingPlansFromUser(userCode).size());
    }

    @Test
    public void testUpdateActivities() {
        UUID userCode = UUID.randomUUID();
        TrainingPlan plan = new TrainingPlan(userCode, MakeItFitDate.of(2024, 4, 4));
        TrainingPlanManager manager = new TrainingPlanManager();
        manager.insertTrainingPlan(plan);

        PushUp pushUp = new PushUp(userCode, MakeItFitDate.of(2024, 3, 1), 10, "", "PushUp", 10, 1);
        plan.addActivity(2, pushUp);

        manager.updateActivities(MakeItFitDate.of(2024, 4, 10), 1.0f);
        // Validação básica de execução, sem exceções
        assertTrue(true);
    }

    @Test
    public void testExtractActivities() {
        UUID userCode = UUID.randomUUID();
        TrainingPlan plan = new TrainingPlan(userCode, MakeItFitDate.of(2024, 4, 4));
        TrainingPlanManager manager = new TrainingPlanManager();
        manager.insertTrainingPlan(plan);

        PushUp pushUp = new PushUp(userCode, MakeItFitDate.of(2024, 3, 20), 10, "", "PushUp", 10, 1);
        plan.addActivity(2, pushUp);

        var activities = manager.extractActivities(MakeItFitDate.of(2024, 4, 1), userCode);
        assertEquals(1, activities.size());
    }


}