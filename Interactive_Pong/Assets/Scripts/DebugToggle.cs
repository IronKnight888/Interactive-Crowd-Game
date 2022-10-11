using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DebugToggle : MonoBehaviour
{
    [SerializeField]
    private Toggle selectedToggle;
    // Start is called before the first frame update
    void Start()
    {
        //selectedToggle = GetComponent<Toggle>();

        selectedToggle.onValueChanged.AddListener(delegate {
            ToggleValueChangedOccured(selectedToggle);
        });
    }

    // Update is called once per frame
    void ToggleValueChangedOccured(Toggle tglValue){
        Debug.Log("current val is: " + tglValue.isOn);
        if (tglValue.isOn == true){
            DebugScript.DebugMode = true;
        }
        else if (tglValue.isOn == false){
            DebugScript.DebugMode = false;
        }
    }
}
