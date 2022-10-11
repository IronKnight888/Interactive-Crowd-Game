using UnityEngine;
using UnityEngine.SceneManagement;

public class Menu : MonoBehaviour
{
    public void PlayNormal()
    {
        SceneManager.LoadScene("Pong");
        GameModeSetter.GameMode = "Normal";
    }

    public void PlayHard()
    {
        SceneManager.LoadScene("Pong");
        GameModeSetter.GameMode = "Hard";
    }

    public void PlayFlashlight()
    {
        SceneManager.LoadScene("Pong");
        GameModeSetter.GameMode = "Flashlight";
    }

    public void PlayFlashlightHard()
    {
        SceneManager.LoadScene("Pong");
        GameModeSetter.GameMode = "FlashlightHard";
    }
}
