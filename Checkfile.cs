using System.Collections;
using System.IO;
using UnityEngine;

public class Ckeckfile : MonoBehaviour
{
    public GameObject textObject;  // Assign your Text GameObject in the Inspector
    private string filePath = "/Users/philippschwarzmann/Desktop/Master HFE/MyNewProject/stress_state.txt";  // Replace with your file path

    private void Start()
    {
        StartCoroutine(CheckFileContents());
    }

    private IEnumerator CheckFileContents()
    {
        while (true)
        {
            if (File.Exists(filePath))
            {
                using (FileStream fs = File.OpenRead(filePath))
                using (StreamReader reader = new StreamReader(fs))
                {
                    string content = reader.ReadToEnd();
                    if (content.Contains("Stress: True"))
                    {
                        textObject.SetActive(true);
                    }
                    else if (content.Contains("Stress: False")) 
                    {
                        textObject.SetActive(false);
                    }
                }
            }

            yield return new WaitForSeconds(2);  // Check every 2 seconds
        }
}
}