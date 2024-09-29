using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ANHYDRALGO
{
    public partial class DateScaleForm : Form
    {
        public int MinYear => (int)numericUpDownMinimum.Value;
        public int MaxYear => (int)numericUpDownMaximum.Value;

        public DateScaleForm()
        {
            InitializeComponent();

            numericUpDownMinimum.ValueChanged += NumericUpDownMin_ValueChanged;
            numericUpDownMaximum.ValueChanged += NumericUpDownMax_ValueChanged;
        }

        private void NumericUpDownMin_ValueChanged(object sender, EventArgs e)
        {
            if (numericUpDownMinimum.Value >= numericUpDownMaximum.Value)
            {
                numericUpDownMinimum.Value = numericUpDownMaximum.Value - 1;
            }
        }

        private void NumericUpDownMax_ValueChanged(object sender, EventArgs e)
        {
            if (numericUpDownMaximum.Value <= numericUpDownMinimum.Value)
            {
                numericUpDownMaximum.Value = numericUpDownMinimum.Value + 1;
            }
        }
    }
}
