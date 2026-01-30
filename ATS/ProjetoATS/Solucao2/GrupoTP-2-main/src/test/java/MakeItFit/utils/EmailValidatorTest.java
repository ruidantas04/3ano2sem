package MakeItFit.utils;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import MakeItFit.utils.MakeItFitDate;
/**
 * The tests for the EmailValidator class.
 *
 * @author  Afonso Santos (a104276), Hélder Gomes (a104100) and Pedro Pereira (a104082)
 * @version (11052024)
 */
public class EmailValidatorTest {

        /**
        * Tests the EmailValidator class method isValid.
        */
        @Test
        public void testIsValid() {
            // Válidos
            assertTrue(EmailValidator.isValidEmail("john@mail.com"));
            assertTrue(EmailValidator.isValidEmail("erica@gmail.com"));
            assertTrue(EmailValidator.isValidEmail("joao.silva@sub.domain.co.uk"));

            // Inválidos
            assertFalse(EmailValidator.isValidEmail("johnmail.com"));
            assertFalse(EmailValidator.isValidEmail("erica@gmailcom"));
            assertFalse(EmailValidator.isValidEmail("john@.com"));
            assertFalse(EmailValidator.isValidEmail("john@com"));
            assertFalse(EmailValidator.isValidEmail("john@com."));
            assertFalse(EmailValidator.isValidEmail(""));

            // Casos extremos
            assertFalse(EmailValidator.isValidEmail(null));
        }

}
