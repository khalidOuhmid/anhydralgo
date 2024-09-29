namespace ANHYDRALGO
{
    partial class ShareForm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(ShareForm));
            this.TwitterShare = new System.Windows.Forms.Button();
            this.FacebookShare = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // TwitterShare
            // 
            this.TwitterShare.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.TwitterShare.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.TwitterShare.FlatAppearance.BorderSize = 0;
            this.TwitterShare.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.TwitterShare.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.TwitterShare.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.TwitterShare.Location = new System.Drawing.Point(52, 54);
            this.TwitterShare.Name = "TwitterShare";
            this.TwitterShare.Size = new System.Drawing.Size(96, 31);
            this.TwitterShare.TabIndex = 27;
            this.TwitterShare.Text = "TWITTER";
            this.TwitterShare.UseVisualStyleBackColor = false;
            this.TwitterShare.Click += new System.EventHandler(this.TwitterShare_Click);
            // 
            // FacebookShare
            // 
            this.FacebookShare.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.FacebookShare.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(116)))), ((int)(((byte)(180)))), ((int)(((byte)(76)))));
            this.FacebookShare.FlatAppearance.BorderSize = 0;
            this.FacebookShare.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.FacebookShare.Font = new System.Drawing.Font("Gill Sans Ultra Bold Condensed", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FacebookShare.ForeColor = System.Drawing.SystemColors.ButtonHighlight;
            this.FacebookShare.Location = new System.Drawing.Point(52, 91);
            this.FacebookShare.Name = "FacebookShare";
            this.FacebookShare.Size = new System.Drawing.Size(96, 31);
            this.FacebookShare.TabIndex = 28;
            this.FacebookShare.Text = "FACEBOOK";
            this.FacebookShare.UseVisualStyleBackColor = false;
            this.FacebookShare.Click += new System.EventHandler(this.FacebookShare_Click);
            // 
            // ShareForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(205, 179);
            this.Controls.Add(this.FacebookShare);
            this.Controls.Add(this.TwitterShare);
            this.Name = "ShareForm";
            this.Text = "ShareForm";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button TwitterShare;
        private System.Windows.Forms.Button FacebookShare;
    }
}