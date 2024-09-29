using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Mail;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ANHYDRALGO
{
    public partial class Windows : Form
    {
        static readonly string vertClair = "#c8df79";
        static readonly string vert = "#74b44c";
        static readonly string vertFonce = "#639543";
        static readonly string vertMoinsClair = "#a7ccac";

        private string currentMapPath;

        static Color vertClair0 = System.Drawing.ColorTranslator.FromHtml(vertClair);
        static Color vert0 = System.Drawing.ColorTranslator.FromHtml(vert);
        static Color vertFonce0 = System.Drawing.ColorTranslator.FromHtml(vertFonce);
        static Color vertMoinsClair0 = System.Drawing.ColorTranslator.FromHtml(vertMoinsClair);

        // cmd
        private readonly string cmdStr;
        private readonly string dataPath;
        private readonly string graphsPath;
        private readonly string linkerOneCountryPath;
        private readonly string linkerMultipleCountriesPath;
        private readonly string dataLinkerByActivity;
        private readonly string mapsPath;
        private string currentGraphName;
        private string graphType = "LINE";

        // sql
        private string datasetActuel = "";
        private List<string> paysActuels = new List<string>();
        private string paysActuel = "";
        private string legendeX = "";
        private string legendeY = "";
        private string graphTitle = "";
        private int anneeMinimale = 1990;
        private int anneeMaximale = 2024;

        public Windows()
        {
            InitializeComponent();
            datasInformations.ForeColor = vertFonce0;
            PerCapitaField.BackColor = vert0;
            FieldsMenu.BackColor = vert0;
            FranceField.BackColor = vert0;
            GermanyField.BackColor = vert0;
            IvoryCoastField.BackColor = vert0;
            CountriesMenu.BackColor = vert0;

            InfosToolTip.BackColor = vert0;
            InfosToolTip.ForeColor = Color.White;

            InfosToolTip.SetToolTip(InfoPictureBox, "Click here to get informations on that project");
            HomeToolTip.SetToolTip(HomePictureBox, "Click here to get to the home menu of our app");
            ServicesToolTip.SetToolTip(ServicesPictureBox, "Click here to get the list of all your services");

            // map
            mapsPath = "../../../../MAPS/";
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "defaultMap.html");
            webBrowser1.Navigate(builtPath);

            // cmd
            cmdStr = "cmd.exe";
            dataPath = "../../../../../Python/";
            graphsPath = "../../pictures/";
            linkerOneCountryPath = dataPath + "dataLinkerSingleCountry.py";
            linkerMultipleCountriesPath = dataPath + "dataLinkerMultipleCountries.py";
            dataLinkerByActivity = dataPath + "dataLinkerByActivity.py";
        }

        private void toolStripMenuItem3_DropDownOpened(object sender, EventArgs e)
        {
            toolStripMenuItem3.ForeColor = vert0;
        }

        private void toolStripMenuItem3_DropDownClosed(object sender, EventArgs e)
        {
            toolStripMenuItem3.ForeColor = Color.White;
        }

        private void toolStripMenuItem1_DropDownOpened_1(object sender, EventArgs e)
        {
            toolStripMenuItem1.ForeColor = vert0;
        }

        private void toolStripMenuItem1_DropDownClosed(object sender, EventArgs e)
        {
            toolStripMenuItem1.ForeColor = Color.White;
        }

        private void toolStripMenuItem4_DropDownOpened(object sender, EventArgs e)
        {
            PeriodMenu.ForeColor = vert0;
        }

        private void toolStripMenuItem4_DropDownClosed(object sender, EventArgs e)
        {
            PeriodMenu.ForeColor = Color.White;
        }

        private void InfosToolTip_Draw(object sender, DrawToolTipEventArgs e)
        {
            Font f = new Font("Impact", 9.0f);
            InfosToolTip.BackColor = vertClair0;
            InfosToolTip.ForeColor = Color.White;
            e.DrawBackground();
            e.DrawBorder();
            e.Graphics.DrawString(e.ToolTipText, f, Brushes.White, new PointF(2, 2));
        }

        private void HomeToolTip_Draw(object sender, DrawToolTipEventArgs e)
        {
            Font f = new Font("Impact", 9.0f);
            InfosToolTip.BackColor = vertClair0;
            InfosToolTip.ForeColor = Color.White;
            e.DrawBackground();
            e.DrawBorder();
            e.Graphics.DrawString(e.ToolTipText, f, Brushes.White, new PointF(2, 2));
        }

        private void ServicesToolTip_Draw(object sender, DrawToolTipEventArgs e)
        {
            Font f = new Font("Impact", 9.0f);
            InfosToolTip.BackColor = vertClair0;
            InfosToolTip.ForeColor = Color.White;
            e.DrawBackground();
            e.DrawBorder();
            e.Graphics.DrawString(e.ToolTipText, f, Brushes.White, new PointF(2, 2));
        }

        private void InfoPictureBox_Click(object sender, EventArgs e)
        {
            Informations informations = new Informations();
            informations.Show();
        }

        private void ServicesPictureBox_Click(object sender, EventArgs e)
        {
            Tuto howtouse = new Tuto();
            howtouse.Show();
        }

        private void HomePictureBox_Click(object sender, EventArgs e)
        {
            Credits credits = new Credits();
            credits.Show();

        }

        private void label2_Click(object sender, EventArgs e)
        {
            Tuto howtouse = new Tuto();
            howtouse.Show();

        }

        /// <summary>
        /// Clears current state and resets the application to default settings upon clicking the reset button.
        /// </summary>
        /// <param name="sender">The object that triggered the event.</param>
        /// <param name="e">Event arguments associated with the event.</param>
        private void ResetButton_Click(object sender, EventArgs e)
        {
            paysActuels.Clear();
            paysActuel = "";
            GraphPictureBox.Visible = false;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "defaultMap.html");
            webBrowser1.Navigate(builtPath);
        }

        /// <summary>
        /// Refreshes the graph display upon clicking the refresh button, based on current data and settings.
        /// </summary>
        /// <param name="sender">The object that triggered the event.</param>
        /// <param name="e">Event arguments associated with the event.</param>
        private void RefreshButton_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            currentGraphName = BuildUpGraphName(); // À compléter
            Console.WriteLine(currentGraphName);
            string graphFilePath = Path.Combine(graphsPath, $"{currentGraphName}.png");
            Console.WriteLine(graphFilePath);

            if (!CurrentGraphExists(currentGraphName))
            {
                Console.WriteLine("Graph actuel n'existe pas");
                Process cmd = GenerateCmd();

                string theCommand = BuildUpSQLCommand(); // À compléter
                string legendeX = GetXLegend(); // À compléter
                string legendeY = GetYLegend(); // À compléter

                string commandLine;
                string selectedFile;

                if (datasetActuel.Equals("By Activity"))
                {
                    selectedFile = dataLinkerByActivity;
                }
                else if (paysActuels.Count() > 1)
                {
                    selectedFile = linkerMultipleCountriesPath;
                }
                else
                {
                    selectedFile = linkerOneCountryPath;
                }

                commandLine = $"python \"{selectedFile}\" \"{theCommand}\" \"{legendeX}\" \"{legendeY}\" \"{currentGraphName}\"";

                Console.WriteLine($"Commande exécutée : {commandLine}");
                CmdAction(commandLine, cmd);

                DisplayResult(graphFilePath);

            }
            else
            {
                Console.WriteLine("Graphique actuel existe");
                DisplayResult(graphFilePath);
            }
            this.Cursor = Cursors.Default;
        }

        /// <summary>
        /// Checks whether a graph image file with the specified name exists in the data path.
        /// If the graph file exists, we won't have to load it from the database again.
        /// </summary>
        /// <param name="graphName">The name of the graph file to check.</param>
        /// <returns>True if the graph file exists; otherwise, false.</returns>
        private Boolean CurrentGraphExists(string graphName)
        {
            string graphFilePath = Path.Combine(dataPath, $"{graphName}.png");
            Console.WriteLine("Chemin attendu : " + graphFilePath);
            return File.Exists(graphFilePath);
        }

        /// <summary>
        /// Constructs a descriptive name for the graph based on current dataset, countries, years, and graph type.
        /// </summary>
        /// <returns>A string representing the constructed graph name.</returns>
        private string BuildUpGraphName()
        {
            StringBuilder sb = new StringBuilder();

            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append("Energies");
            }
            else
            {
                sb.Append("GHG Emissions");
            }

            sb.Append(" in ");
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append(paysActuel + " ");
            }
            else if (paysActuels.Count() < FieldsMenu.DropDownItems.Count)
            {
                foreach (string s in paysActuels)
                {
                    sb.Append(s + " ");
                }
            }
            else
            {
                sb.Append("Global ");
            }

            sb.Append("from ");
            sb.Append(anneeMinimale);
            sb.Append(" to ");
            sb.Append(anneeMaximale);
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append(" " + datasetActuel);
            }
            else
            {
                sb.Append(" by " + datasetActuel);
            }

            sb.Append(", " + graphType + " view");

            return sb.ToString();
        }

        /// <summary>
        /// Retrieves the X-axis legend based on the number of selected countries.
        /// </summary>
        /// <returns>A string representing the X-axis legend.</returns>
        private string GetXLegend()
        {
            string legendX;

            if (paysActuels.Count() > 1)
            {
                legendX = "Global Carbon Footprint";
            }
            else
            {
                legendX = "Date";
            }

            return legendX;
        }

        /// <summary>
        /// Retrieves the Y-axis legend based on the number of selected countries.
        /// </summary>
        /// <returns>A string representing the Y-axis legend.</returns>
        private string GetYLegend()
        {
            string legend;

            if (paysActuels.Count() > 1)
            {
                legend = "Values";
            }
            else
            {
                legend = "CO2"; // TO COMPLETE MAYBE (?)
            }

            return legend;
        }

        /// <summary>
        /// Constructs a SQL query command based on current dataset, selected countries, years, and graph type.
        /// We kept checking for the same conditions to have a coherent construction of a SQL command, so that it's easier to read.
        /// </summary>
        /// <returns>A string representing the constructed SQL query command.</returns>
        private string BuildUpSQLCommand()
        {
            StringBuilder sb = new StringBuilder();

            sb.Append("SELECT ");
            // étudier les éléments à select
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append("DTA_VALEUR, EGY_NOM, PYS_NOM, DAT_DATE");
            }
            else if (paysActuels.Count() > 1) // abs: value | ord : country
            {
                sb.Append("DAT_DATE, PYS_NOM, DTA_VALEUR");
            }
            else // abs: date | ord: value
            {
                sb.Append("DAT_DATE, DTA_VALEUR");
            }

            sb.Append(" ");
            sb.Append("FROM T_DATA_DTA ");

            // étudier les jointures
            sb.Append("INNER JOIN T_PAYS_PYS ON T_DATA_DTA.PYS_ID = T_PAYS_PYS.PYS_ID ");
            sb.Append("INNER JOIN T_DATE_DAT ON T_DATE_DAT.DAT_ID = T_DATA_DTA.DAT_ID ");
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append("INNER JOIN T_ENERGY_EGY ON T_ENERGY_EGY.EGY_ID = T_DATA_DTA.EGY_ID ");
            }

            sb.Append("WHERE (");
            // étudier les conditions
            // Pays
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append("PYS_NOM = '" + paysActuel + "' ");
            }
            else
            {
                for (int i = 0; i < paysActuels.Count(); i++)
                {
                    if (i == 0)
                    {
                        sb.Append("PYS_NOM = '" + paysActuels[i] + "' ");
                    }
                    else
                    {
                        sb.Append("OR PYS_NOM = '" + paysActuels[i] + "' ");
                    }
                }
            }

            sb.Append(") ");

            // Dataset
            switch (datasetActuel)
            {
                case "Per GDP":
                    sb.Append("AND DTA_NOM = 'GDP'");
                    break;
                case "Total":
                    // TO DO
                    break;
                case "By Activity":
                    // OK! La liaison avec la table T_ACTIVITY_ACT gère cette condition
                    break;
                case "Per Capita":
                    sb.Append("AND DTA_NOM = 'Annual CO2 emissions per capita'");
                    break;
            }

            sb.Append(" ");

            // Energies
            if (datasetActuel.Equals("By Activity"))
            {
                sb.Append("AND EGY_NOM IN ('Coal', 'Gas', 'Hydro', 'Solar', 'Wind', 'Oil', 'Nuclear', 'Other renewables excluding bioenergy', 'Bioenergy')");
            }

            sb.Append(" ");
            // Période
            // Ajouter la condition pour la date minimale
            sb.Append("AND DAT_DATE >= '");
            sb.Append(anneeMinimale);
            sb.Append("-01-01' ");

            // Ajouter la condition pour la date maximale
            sb.Append("AND DAT_DATE <= '");
            sb.Append(anneeMaximale);
            sb.Append("-12-31' ");

            sb.Append("ORDER BY T_DATE_DAT.DAT_DATE");

            sb.Append(" ");


            return sb.ToString();
        }

        private void Windows_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void webBrowser1_DocumentCompleted(object sender, WebBrowserDocumentCompletedEventArgs e)
        {
            this.Cursor = Cursors.Default;
        }

        private void button5_Click(object sender, EventArgs e)
        {

        }

        private void button6_Click(object sender, EventArgs e)
        {

        }

        private void hScrollBar1_Scroll(object sender, ScrollEventArgs e)
        {

        }

        /// <summary>
        /// Displays the generated graph image in a PictureBox control based on the specified image file.
        /// </summary>
        /// <param name="fileNameImage">The path to the graph image file to display.</param>
        private void DisplayResult(string fileNameImage)
        {
            try
            {
                // permet de fermer/libérer les ressources utilisées à la fin du bloc
                // ici on utilise et libère un fichier d'image
                using (Image img = Image.FromFile(fileNameImage))
                {
                    GraphPictureBox.Image = new Bitmap(img);
                    GraphPictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
                    GraphPictureBox.Visible = true;
                }
                Console.WriteLine("Image loaded successfully.");
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine("Image file not found: " + fileNameImage);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
        }

        /// <summary>
        /// Executes a command line action using a specified command line string and waits for completion.
        /// </summary>
        /// <param name="line">The command line string to execute.</param>
        /// <param name="cmd">The Process object representing the command line process.</param>
        private void CmdAction(string line, Process cmd)
        {
            cmd.StandardInput.WriteLine(line);
            cmd.StandardInput.Flush();
            cmd.StandardInput.Close();
            cmd.WaitForExit();
        }

        /// <summary>
        /// Generates and starts a new command line process with specified settings.
        /// </summary>
        /// <returns>A Process object representing the newly started command line process.</returns>
        private Process GenerateCmd()
        {
            Process cmd = new Process();
            cmd.StartInfo.FileName = cmdStr;
            cmd.StartInfo.RedirectStandardInput = true;
            cmd.StartInfo.RedirectStandardOutput = true;
            cmd.StartInfo.CreateNoWindow = true;
            cmd.StartInfo.UseShellExecute = false;
            cmd.Start();
            return cmd;
        }

        /// <summary>
        /// Updates the state of the ToolStripMenuItem based on its current checked state and the state of its parent menu.
        /// </summary>
        /// <param name="theButton">The ToolStripMenuItem whose state needs to be updated.</param>
        private void UpdateButtonState(ToolStripMenuItem theButton)
        {
            ToolStripDropDownMenu parentMenu = theButton.GetCurrentParent() as ToolStripDropDownMenu;

            if (parentMenu != null)
            {
                foreach (ToolStripItem item in parentMenu.Items)
                {
                    if (item is ToolStripMenuItem menuItem && menuItem != theButton)
                    {
                        menuItem.Checked = false;
                    }
                }
            }

            // Changer l'état du bouton actuel
            theButton.Checked = !theButton.Checked;
        }

        /// <summary>
        /// Turns off the checked state for all other ToolStripMenuItems in the same parent menu as the specified ToolStripMenuItem.
        /// </summary>
        /// <param name="theItem">The ToolStripMenuItem whose parent menu's other items need their checked state turned off.</param>
        private void TurnOffAllOtherButtons(ToolStripMenuItem theItem)
        {
            ToolStripDropDownMenu parentMenu = theItem.GetCurrentParent() as ToolStripDropDownMenu;

            if (parentMenu != null)
            {
                foreach (ToolStripItem item in parentMenu.Items)
                {
                    if (item is ToolStripMenuItem menuItem && menuItem != theItem)
                    {
                        menuItem.Checked = false;
                    }
                }
            }
        }

        /// <summary>
        /// Updates the list of currently selected countries based on the checked state of ToolStripMenuItems in the FieldsMenu.
        /// </summary>
        private void UpdateSelectedCountries()
        {
            if (GlobalField.Checked)
            {
                foreach (ToolStripItem item in FieldsMenu.DropDownItems)
                {
                    if (item is ToolStripMenuItem menuItem)
                    {
                        menuItem.Enabled = false;
                        menuItem.Checked = false;
                        paysActuels.Add(item.Text);
                    }
                }
            }
            else
            {
                foreach (ToolStripItem item in FieldsMenu.DropDownItems)
                {
                    if (item is ToolStripMenuItem menuItem)
                    {
                        if (!menuItem.Enabled)
                        {
                            menuItem.Enabled = true;
                        }
                        if (menuItem.Checked && !paysActuels.Contains(menuItem.Text))
                        {
                            // pour chaque fils s'il est coché, le rajouter à la liste
                            paysActuels.Add(menuItem.Text);
                        }
                        if (!menuItem.Checked && paysActuels.Contains(menuItem.Text))
                        {
                            // pour chaque fils s'il est décoché, vérifier qu'il n'est pas dans la liste des pays et si c'est le cas, le retirer
                            paysActuels.Remove(menuItem.Text);
                        }
                    }

                }

            }

        }


        private void FranceField_Click(object sender, EventArgs e)
        {
            paysActuel = "France";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(FranceField);
            }
        }

        private void GermanyField_Click(object sender, EventArgs e)
        {
            paysActuel = "Germany";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(GermanyField);
            }
        }

        private void ChinaField_Click(object sender, EventArgs e)
        {
            paysActuel = "China";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(ChinaField);
            }
        }

        private void IndiaField_Click(object sender, EventArgs e)
        {
            paysActuel = "India";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(IndiaField);
            }
        }

        private void UnitedStatesField_Click(object sender, EventArgs e)
        {
            paysActuel = "United States";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(UnitedStatesField);
            }
        }

        private void DenmarkField_Click(object sender, EventArgs e)
        {
            paysActuel = "Denmark";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(DenmarkField);
            }
        }

        private void IvoryCoastField_Click(object sender, EventArgs e)
        {
            paysActuel = "Ivory Coast";
            UpdateSelectedCountries();
            if (datasetActuel.Equals("By Activity"))
            {
                TurnOffAllOtherButtons(IvoryCoastField);
            }
        }

        private void UpdateCurrentDataset(ToolStripMenuItem theItem, string datasetName)
        {
            if (theItem.Checked)
            {
                datasetActuel = datasetName;
            }
            else
            {
                datasetActuel = "";
            }
        }

        private void TotalField_Click(object sender, EventArgs e)
        {
            UpdateButtonState(TotalField);
            UpdateCurrentDataset(TotalField, "Total");
        }

        private void PerCapitaField_Click(object sender, EventArgs e)
        {
            UpdateButtonState(PerCapitaField);
            UpdateCurrentDataset(PerCapitaField, "Per Capita");
        }

        private void PerGDPField_Click(object sender, EventArgs e)
        {
            UpdateButtonState(PerGDPField);
            UpdateCurrentDataset(PerGDPField, "Per GDP");
        }

        private void ByActivityField_Click(object sender, EventArgs e)
        {
            UpdateButtonState(ByActivityField);
            UpdateCurrentDataset(ByActivityField, "By Activity");
            if (ByActivityField.Checked)
            {
                GlobalField.Enabled = false;
                GlobalField.Checked = false;
                TotalField.Enabled = false;
                PerGDPField.Enabled = false;
                PerCapitaField.Enabled = false;
                LineType.Checked = false;
                LineType.Enabled = false;
                PieType.Checked = true;
                PieType.Enabled = true;
                graphType = PieType.Text;
                foreach (ToolStripItem item in FieldsMenu.DropDownItems)
                {
                    if (item is ToolStripMenuItem menuItem)
                    {
                        menuItem.Enabled = true;
                        menuItem.Checked = false;
                    }
                }
            }
            else
            {
                GlobalField.Enabled = true;
                TotalField.Enabled = true;
                PerGDPField.Enabled = true;
                PerCapitaField.Enabled = true;
                LineType.Checked = true;
                LineType.Enabled = true;
                PieType.Checked = false;
                PieType.Enabled = false;
                graphType = LineType.Text;
                foreach (ToolStripItem item in FieldsMenu.DropDownItems)
                {
                    if (item is ToolStripMenuItem menuItem)
                    {
                        menuItem.Enabled = true;
                        menuItem.Checked = false;
                    }
                }
            }
        }

        private void GlobalField_Click(object sender, EventArgs e)
        {
            UpdateSelectedCountries();
        }

        private void PeriodMenu_Click(object sender, EventArgs e)
        {
            using (DateScaleForm intervalForm = new DateScaleForm())
            {
                if (intervalForm.ShowDialog() == DialogResult.OK)
                {
                    anneeMinimale = intervalForm.MinYear;
                    anneeMaximale = intervalForm.MaxYear;
                }
            }
        }

        private void HistogramType_Click(object sender, EventArgs e)
        {
            graphType = "HISTOGRAM";
            UpdateButtonState(HistogramType);
        }

        private void BarType_Click(object sender, EventArgs e)
        {
            graphType = "BAR";
            UpdateButtonState(BarType);
        }

        private void PieType_Click(object sender, EventArgs e)
        {
            graphType = "PIE";
            UpdateButtonState(PieType);
        }

        private void LineType_Click(object sender, EventArgs e)
        {
            graphType = "LINE";
            UpdateButtonState(LineType);
        }

        private void cO2ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "30YoCO2.html");
            OpenFileWithConfirmation(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void pIBToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "30YPIB.html");
            OpenFileWithConfirmation(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void populationToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "30Y_Population.html");
            OpenFileWithConfirmation(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void pluvioToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapPluvio.html");
            currentMapPath = builtPath;
            webBrowser1.Navigate(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void pIBToolStripMenuItem2_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapPIB.html");
            currentMapPath = builtPath;
            webBrowser1.Navigate(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void populationToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapPopulation.html");
            currentMapPath = builtPath;
            webBrowser1.Navigate(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void temperaturesToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapTemp.html");
            currentMapPath = builtPath;
            webBrowser1.Navigate(builtPath);
            this.Cursor = Cursors.Default;
        }

        private void pLUVIOCO2TEMPERATURESToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "map_with_layers.html");
            webBrowser1.Navigate(builtPath);
            currentMapPath = builtPath;
            this.Cursor = Cursors.Default;
        }

        private void cH4ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapFossilsCH4.html");
            webBrowser1.Navigate(builtPath);
            currentMapPath = builtPath;
            this.Cursor = Cursors.Default;
        }

        private void cO2ToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapFossilsCO2.html");
            webBrowser1.Navigate(builtPath);
            currentMapPath = builtPath;
            this.Cursor = Cursors.Default;
        }

        private void n2OToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
            string builtPath = Path.Combine(Application.StartupPath, mapsPath + "mapFossilsN2O.html");
            webBrowser1.Navigate(builtPath);
            currentMapPath = builtPath;
            this.Cursor = Cursors.Default;
        }

        private void OpenFileWithConfirmation(string cheminFichier)
        {
            // Demander la confirmation de l'utilisateur
            DialogResult result = MessageBox.Show("Are you sure that you want to open this map in your browser?", "Confirmation", MessageBoxButtons.YesNo, MessageBoxIcon.Question);

            // Vérifier la réponse de l'utilisateur
            if (result == DialogResult.Yes)
            {
                // Ouvrir le fichier HTML dans le navigateur par défaut
                try
                {
                    Process.Start(cheminFichier);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Error : " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }

        private void WebBrowser1_Navigating(object sender, WebBrowserNavigatingEventArgs e)
        {
            this.Cursor = Cursors.WaitCursor;
        }

        private void Windows_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
            {
                DeleteFilesInDirectory(graphsPath);
            }
        }

        private void DeleteFilesInDirectory(string directoryPath)
        {
            try
            {
                if (Directory.Exists(directoryPath))
                {
                    string[] files = Directory.GetFiles(directoryPath);

                    foreach (string file in files)
                    {
                        File.Delete(file);
                        Console.WriteLine($"Deleted file: {file}");
                    }

                    Console.WriteLine("All files deleted successfully.");
                }
                else
                {
                    Console.WriteLine($"Directory '{directoryPath}' does not exist.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error deleting files in directory '{directoryPath}': {ex.Message}");
            }
        }

        private void GraphTypeMenu_DropDownOpened(object sender, EventArgs e)
        {
            GraphTypeMenu.ForeColor = vert0;
        }

        private void GraphTypeMenu_DropDownClosed(object sender, EventArgs e)
        {
            GraphTypeMenu.ForeColor = Color.White;
        }

        private void mAPSToolStripMenuItem_DropDownOpened(object sender, EventArgs e)
        {
            mAPSToolStripMenuItem.ForeColor = vert0;
        }

        private void mAPSToolStripMenuItem_DropDownClosed(object sender, EventArgs e)
        {
            mAPSToolStripMenuItem.ForeColor = Color.White;
        }

        private void DwnButton_Click(object sender, EventArgs e)
        {
            string graphFilePath = Path.Combine(graphsPath, $"{currentGraphName}.png");
            PromptUserToSaveFile(graphFilePath);
        }

        private void PromptUserToSaveFile(string graphFilePath)
        {
            using (SaveFileDialog saveFileDialog = new SaveFileDialog())
            {
                saveFileDialog.Filter = "PNG Files|*.png";
                saveFileDialog.Title = "Save Graph As";
                saveFileDialog.FileName = currentGraphName;

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string destinationPath = saveFileDialog.FileName;
                    try
                    {
                        File.Copy(graphFilePath, destinationPath, true);
                        MessageBox.Show("Graphique téléchargé avec succès!", "Téléchargement terminé", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Erreur lors du téléchargement du graphique: {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        private void MapSave_Click(object sender, EventArgs e)
        {
            SaveMap(currentMapPath);
        }

        private void SaveMap(string mapPath)
        {
            if (mapPath == null)
            {
                MessageBox.Show("Chargez une carte pour la sauvegarder !");
                return;
            }

            using (SaveFileDialog saveFileDialog = new SaveFileDialog())
            {
                saveFileDialog.Filter = "HTML Files|*.html";
                saveFileDialog.Title = "Save Map As";
                saveFileDialog.FileName = Path.GetFileName(mapPath);

                if (saveFileDialog.ShowDialog() == DialogResult.OK)
                {
                    string destinationPath = saveFileDialog.FileName;
                    try
                    {
                        File.Copy(mapPath, destinationPath, true);
                        MessageBox.Show("Carte sauvegardée avec succès!", "Sauvegarde terminée", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Erreur lors de la sauvegarde de la carte: {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        private void ShareButton_Click(object sender, EventArgs e)
        {
            string graphFilePath = Path.Combine(graphsPath, $"{currentGraphName}.png");

            if (!File.Exists(graphFilePath))
            {
                MessageBox.Show("Le graphique n'existe pas. Veuillez d'abord charger un graphique.");
                return;
            }

            using (var shareForm = new ShareForm(graphFilePath))
            {
                shareForm.ShowDialog();
            }
        }
    }
}
