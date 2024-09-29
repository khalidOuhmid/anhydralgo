namespace ANHYDRALGO
{
    partial class Informations
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Informations));
            this.InfoPictureBox = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.InfoPictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // InfoPictureBox
            // 
            this.InfoPictureBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.InfoPictureBox.BackColor = System.Drawing.Color.Transparent;
            this.InfoPictureBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.InfoPictureBox.Cursor = System.Windows.Forms.Cursors.Hand;
            this.InfoPictureBox.Image = ((System.Drawing.Image)(resources.GetObject("InfoPictureBox.Image")));
            this.InfoPictureBox.InitialImage = ((System.Drawing.Image)(resources.GetObject("InfoPictureBox.InitialImage")));
            this.InfoPictureBox.Location = new System.Drawing.Point(69, 9);
            this.InfoPictureBox.Margin = new System.Windows.Forms.Padding(0);
            this.InfoPictureBox.Name = "InfoPictureBox";
            this.InfoPictureBox.Size = new System.Drawing.Size(126, 119);
            this.InfoPictureBox.TabIndex = 7;
            this.InfoPictureBox.TabStop = false;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Font = new System.Drawing.Font("Impact", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label1.Location = new System.Drawing.Point(25, 143);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(224, 190);
            this.label1.TabIndex = 8;
            this.label1.Text = resources.GetString("label1.Text");
            this.label1.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // Informations
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.ClientSize = new System.Drawing.Size(272, 335);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.InfoPictureBox);
            this.DoubleBuffered = true;
            this.Name = "Informations";
            this.Text = "InformationsForms";
            this.Load += new System.EventHandler(this.Informations_Load);
            ((System.ComponentModel.ISupportInitialize)(this.InfoPictureBox)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        protected System.Windows.Forms.PictureBox InfoPictureBox;
        private System.Windows.Forms.Label label1;
    }
}