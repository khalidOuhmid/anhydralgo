using System;
using System.Diagnostics;
using System.Windows.Forms;

namespace ANHYDRALGO
{
    public partial class ShareForm : Form
    {
        private string twitterShareUrl;
        private string facebookShareUrl;

        public ShareForm(string graphFilePath)
        {
            InitializeComponent();
            SetupShareUrls(graphFilePath);
        }

        private void SetupShareUrls(string graphFilePath)
        {
            string urlEncodedGraphPath = Uri.EscapeDataString(graphFilePath);

            twitterShareUrl = $"https://twitter.com/intent/tweet?text=Check%20out%20this%20graph!&url={urlEncodedGraphPath}";
            facebookShareUrl = $"https://www.facebook.com/sharer/sharer.php?u={urlEncodedGraphPath}";
        }

        private void TwitterShare_Click(object sender, EventArgs e)
        {
            Process.Start(new ProcessStartInfo(twitterShareUrl) { UseShellExecute = true });
        }

        private void FacebookShare_Click(object sender, EventArgs e)
        {
            Process.Start(new ProcessStartInfo(facebookShareUrl) { UseShellExecute = true });
        }
    }
}
