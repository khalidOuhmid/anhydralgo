namespace ANHYDRALGO
{
    partial class Tuto
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Tuto));
            this.Title2 = new System.Windows.Forms.Label();
            this.HomePictureBox = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.HomePictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // Title2
            // 
            this.Title2.BackColor = System.Drawing.Color.Transparent;
            this.Title2.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 20.25F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Title2.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.Title2.Location = new System.Drawing.Point(171, 132);
            this.Title2.Name = "Title2";
            this.Title2.Size = new System.Drawing.Size(134, 36);
            this.Title2.TabIndex = 4;
            this.Title2.Text = "TUTORIAL";
            this.Title2.Click += new System.EventHandler(this.Title2_Click);
            // 
            // HomePictureBox
            // 
            this.HomePictureBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.HomePictureBox.BackColor = System.Drawing.Color.Transparent;
            this.HomePictureBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.HomePictureBox.Cursor = System.Windows.Forms.Cursors.Hand;
            this.HomePictureBox.Image = ((System.Drawing.Image)(resources.GetObject("HomePictureBox.Image")));
            this.HomePictureBox.InitialImage = ((System.Drawing.Image)(resources.GetObject("HomePictureBox.InitialImage")));
            this.HomePictureBox.Location = new System.Drawing.Point(188, 9);
            this.HomePictureBox.Margin = new System.Windows.Forms.Padding(0);
            this.HomePictureBox.Name = "HomePictureBox";
            this.HomePictureBox.Size = new System.Drawing.Size(105, 111);
            this.HomePictureBox.TabIndex = 5;
            this.HomePictureBox.TabStop = false;
            // 
            // label1
            // 
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Font = new System.Drawing.Font("Impact", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.label1.Location = new System.Drawing.Point(84, 189);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(318, 354);
            this.label1.TabIndex = 9;
            this.label1.Text = resources.GetString("label1.Text");
            this.label1.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            // 
            // Tuto
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch;
            this.ClientSize = new System.Drawing.Size(477, 583);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.HomePictureBox);
            this.Controls.Add(this.Title2);
            this.DoubleBuffered = true;
            this.Name = "Tuto";
            this.Text = "Tuto";
            ((System.ComponentModel.ISupportInitialize)(this.HomePictureBox)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label Title2;
        protected System.Windows.Forms.PictureBox HomePictureBox;
        private System.Windows.Forms.Label label1;
    }
}