using UnityEngine;

public class ScoreTracker : MonoBehaviour
{
    private static GameObject instance;

    public int p1_score;
    public int p2_score;
    public string winner;

    public GameManager gameManager;

    private void Awake()
    {
        DontDestroyOnLoad(gameObject);
        if (instance == null)
        {
            instance = gameObject;
        }
        else
        {
            Destroy(gameObject);
        }
    }
}