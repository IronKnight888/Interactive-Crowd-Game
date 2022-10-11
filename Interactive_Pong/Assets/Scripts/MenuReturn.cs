using UnityEngine.SceneManagement;
using UnityEngine;

public class MenuReturn : MonoBehaviour
{
    // Start is called before the first frame update
    public void Return()
    {
        SceneManager.LoadScene("Menu");
    }

}
