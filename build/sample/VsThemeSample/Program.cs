namespace VsThemeSample;

/// <summary>Small console app used to preview the Visual Studio 2022 theme in Rider.</summary>
public sealed class Program
{
    private const string Greeting = "Visual Studio 2022 theme preview";

    public static async Task Main(string[] args)
    {
        var surfaces = new List<string> { "toolbar", "solution explorer", "editor", "status bar" };

        foreach (var surface in surfaces)
        {
            Console.WriteLine($"{Greeting}: {surface}");
        }

        await Task.Delay(0);
    }
}
