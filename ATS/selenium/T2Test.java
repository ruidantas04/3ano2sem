import org.junit.Before;
import org.junit.After;
import org.junit.Test;
import static org.junit.Assert.assertThat;
import static org.junit.Assert.assertTrue;
import static org.hamcrest.CoreMatchers.is;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.Dimension;
import java.util.*;
import java.util.regex.Pattern;

public class T2Test {
  private WebDriver driver;
  private Map<String, Object> vars;

  @Before
  public void setUp() {
    driver = new ChromeDriver();
    vars = new HashMap<String, Object>();
  }

  @After
  public void tearDown() {
    driver.quit();
  }

  @Test
  public void t2() {
    driver.get("https://www.calculator.net/");
    driver.manage().window().setSize(new Dimension(1552, 832));
    assertThat(driver.findElement(By.cssSelector("h1")).getText(), is("Free Online Calculators"));

    driver.findElement(By.linkText("Math Calculators")).click();
    driver.findElement(By.linkText("Random Number Generator")).click();

    // Limpar o campo antes de digitar o número
    driver.findElement(By.name("supper")).click();
    driver.findElement(By.name("supper")).clear();  // Limpa o campo
    driver.findElement(By.name("supper")).sendKeys("10");  // Digita "10"

    driver.findElement(By.name("x")).click();

    // Usando Pattern.matches para verificar se o número gerado está entre 0 e 10
    String resultText = driver.findElement(By.cssSelector(".verybigtext")).getText();
    assertTrue("O número gerado deve estar entre 0 e 10", Pattern.matches("^[0-9]$|^10$", resultText));
  }
}
