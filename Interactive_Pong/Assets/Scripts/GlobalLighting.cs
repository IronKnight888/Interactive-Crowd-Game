using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class GlobalLighting : MonoBehaviour
{
    UnityEngine.Rendering.Universal.Light2D GlobalLight;
    void Start()
    {
        if (GameModeSetter.GameMode == "Flashlight" || GameModeSetter.GameMode == "FlashlightHard"){
            StartCoroutine(LightCoroutine());
        }
        
    }

    IEnumerator LightCoroutine()
    {
        Debug.Log("Started Coroutine at timestamp : " + Time.time);

        yield return new WaitForSeconds(1);

        GlobalLight = GetComponent<UnityEngine.Rendering.Universal.Light2D>();
        GlobalLight.intensity = 0f;

        Debug.Log("Finished Coroutine at timestamp : " + Time.time);
    }
}
