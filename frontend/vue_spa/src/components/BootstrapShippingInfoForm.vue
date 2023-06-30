<template>

  <ul class="customer-info-details border-top">

              <li>
                <div class="row row-cols-auto ms-0 me-0 pt-2 clearfix">

                  <div class="col-md-3 pt-2 pe-1 ps-0">

                    <label for="firstName" class="form-label" >First name</label>
                    <div class="input-group">
                      <input type="text"
                             id="first-name"
                             name="firstName"
                             class="form-control"
                             placeholder="e.g. Jack"
                             aria-label="First name"
                             aria-describedby="firstName"
                             autocomplete="given-name"
                      >
                    </div>

                  </div>

                  <div class="col-md-3 ps-3 pt-2 pe-1 related-field">

                    <label for="lastName" class="form-label">Last name</label>
                    <div class="input-group">
                      <input type="text"
                             id="last-name"
                             name="lastName"
                             class="form-control"
                             placeholder="e.g. Doe"
                             aria-label="Last name"
                             aria-describedby="lastName"
                             autocomplete="family-name"
                      >
                    </div>

                  </div>

                </div>
              </li>

              <li>
                <div class="row ms-0 me-0 pt-2 clearfix">
                  <div class="col-md-6 pt-2 ps-0 pe-1">

                    <label for="email" class="form-label">Email</label>
                    <div class="input-group">
                      <!--                      <span class="input-group-text" id="basic-addon1">@</span>-->
                      <input type="email"
                             id="email"
                             name="email"
                             class="form-control"
                             placeholder="e.g. Jack.Doe@xyz.com"
                             aria-label="Email"
                             aria-describedby="email"
                             autocomplete="email"
                      >
                    </div>

                  </div>
                </div>
              </li>

              <li>
                <div class="row ms-0 me-0 pt-2 clearfix">
                  <div class="col-md-6 pt-2 ps-0 pe-1">

                    <label for="phoneNumber" class="form-label">Phone number</label>
                    <div class="input-group">
                      <input type="tel"
                             id="phone-number"
                             name="phoneNumber"
                             class="form-control"
                             placeholder="e.g. 00964112234567"
                             aria-label="Phone number"
                             aria-describedby="phoneNumber"
                             autocomplete="tel"
                      >
                    </div>

                  </div>
                </div>
              </li>

              <li>
                <div class="row ms-0 me-0 pt-2 clearfix">
                  <div class="col-md-6 pt-2 ps-0 pe-1">

                    <label for="address1" class="form-label">Address 1</label>
                    <div class="input-group">
                      <input type="text"
                             id="address-1"
                             name="address1"
                             class="form-control"
                             placeholder="e.g, 13, Main Str."
                             aria-label="Address 1"
                             aria-describedby="address1"
                             autocomplete="address-line1"
                      >
                    </div>

                  </div>
                </div>
              </li>

              <li>
                <div class="row ms-0 me-0 pt-2 clearfix">
                  <div class="col-md-6 pt-2 ps-0 pe-1">

                    <label for="address2" class="form-label">Address 2</label>
                    <div class="input-group">
                      <input type="text"
                             id="address-2"
                             name="address2"
                             class="form-control"
                             placeholder="e.g, Apt/Suite/Building"
                             aria-label="Address 2"
                             aria-describedby="address2"
                             autocomplete="address-line2"
                      >
                    </div>

                  </div>
                </div>
              </li>

              <li>
                <div class="row row-cols-auto ms-0 me-0 pt-2 clearfix">

                  <div class="col-md-3 pt-2 pe-1 ps-0">

                    <label for="country" class="form-label">Country</label>
                    <select class="form-select" id="country" name="country" autocomplete="country-name">
                      <option selected>Choose...</option>
                      <option value="IQ">Iraq</option>
                      <option value="US">United States of America</option>
                      <option value="UK">United kingdom</option>
                    </select>

                  </div>

                  <div class="col-md-3 pt-2 pe-1 ps-3 related-field">

                    <label for="region" class="form-label">Region</label>
                    <div class="input-group">
                      <input type="text"
                             id="region"
                             name="region"
                             class="form-control"
                             placeholder="e.g, State/Province"
                             aria-label="Region"
                             aria-describedby="region"
                             autocomplete="region"
                      >
                    </div>

                  </div>

                </div>
              </li>

              <li>
                <div class="row row-cols-auto ms-0 me-0 pt-2 clearfix">

                  <div class="col-md-3 pt-2 pe-1 ps-0">

                    <label for="city" class="form-label">City</label>
                    <div class="input-group">
                      <input type="text"
                             id="city"
                             name="city"
                             class="form-control"
                             aria-label="City"
                             aria-describedby="city"
                             autocomplete="city"
                      >
                    </div>

                  </div>

                  <div class="col-md-3 pt-2 pe-1 ps-3 related-field">

                    <label for="postalCode" class="form-label">Postal code</label>
                    <div class="input-group">
                      <input type="text"
                             id="postal-code"
                             name="postalCode"
                             class="form-control"
                             aria-label="Postal code"
                             aria-describedby="postalCode"
                             autocomplete="postal-code"
                      >
                    </div>

                  </div>

                </div>
              </li>

            </ul>

</template>

<script>
export default {
  name: "bootstrapShippingInfoForm"
}
</script>

<style lang="scss" scoped>

$main-color: #0F1111;

.customer-info-details{
  list-style: none;
  padding-top: 8px;
  padding-left: 0;
}

hr{
    margin-top: 2rem;
}

label{
  font-weight: 400;
  color: $main-color;
}

label, option {
  font-size: 14px;
}
input::placeholder {
  font-size: 13px;
}

// for phones and tablets
@media(max-width:767px){
  .related-field{
    padding-left: 0!important;
  }
  input::placeholder {
    font-size: 12px;
  }
}
// for big screens
@media(min-width:768px) {
  .related-field {
    padding-left: 10px !important;
  }
}
</style>